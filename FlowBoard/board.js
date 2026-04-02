// FlowBoard Board Renderer — HTML5 drag-and-drop Kanban board
(function () {
  'use strict';

  // ── Column definitions ────────────────────────────────────────────────
  var COLUMNS = [
    { status: 'backlog',     label: 'Backlog',      color: '#64748B' },
    { status: 'todo',        label: 'To Do',        color: '#7C6BF2' },
    { status: 'in_progress', label: 'In Progress',  color: '#F59E0B' },
    { status: 'review',      label: 'Review',       color: '#06B6D4' },
    { status: 'done',        label: 'Done',         color: '#22C55E' }
  ];

  // ── Priority badge config ─────────────────────────────────────────────
  var PRIORITY_CONFIG = {
    critical: { label: 'Critical', bg: '#FEE2E2', text: '#DC2626', dot: '#DC2626' },
    high:     { label: 'High',     bg: '#FEF3C7', text: '#D97706', dot: '#F59E0B' },
    medium:   { label: 'Medium',   bg: '#DBEAFE', text: '#1D4ED8', dot: '#3B82F6' },
    low:      { label: 'Low',      bg: '#F1F5F9', text: '#64748B', dot: '#94A3B8' }
  };

  // ── Internal state ────────────────────────────────────────────────────
  var _currentFilters = { project_id: null, assignee_id: null, priority: null, query: null };

  // ── Helpers ───────────────────────────────────────────────────────────

  function escHtml(str) {
    if (str == null) return '';
    return String(str)
      .replace(/&/g, '&amp;')
      .replace(/</g, '&lt;')
      .replace(/>/g, '&gt;')
      .replace(/"/g, '&quot;')
      .replace(/'/g, '&#39;');
  }

  function getMemberById(id) {
    var members = window.store.members;
    for (var i = 0; i < members.length; i++) {
      if (members[i].id === id) return members[i];
    }
    return null;
  }

  function isOverdue(dueDateStr) {
    if (!dueDateStr) return false;
    var today = new Date().toISOString().slice(0, 10);
    return dueDateStr < today;
  }

  function formatDate(dateStr) {
    if (!dateStr) return '';
    // dateStr is YYYY-MM-DD — parse as local date to avoid UTC offset shift
    var parts = dateStr.split('-');
    if (parts.length !== 3) return dateStr;
    var d = new Date(
      parseInt(parts[0], 10),
      parseInt(parts[1], 10) - 1,
      parseInt(parts[2], 10)
    );
    return d.toLocaleDateString(undefined, { month: 'short', day: 'numeric' });
  }

  // Apply active filters to a task array.
  // Supports query-string search across title, description, and tags.
  function applyFilters(tasks, filters) {
    if (!filters) return tasks;
    return tasks.filter(function (t) {
      if (filters.project_id  && t.project_id  !== filters.project_id)  return false;
      if (filters.assignee_id && t.assignee_id !== filters.assignee_id) return false;
      if (filters.priority    && t.priority    !== filters.priority)     return false;
      if (filters.query) {
        var q = filters.query.toLowerCase();
        var inTitle = t.title && t.title.toLowerCase().indexOf(q) !== -1;
        var inDesc  = t.description && t.description.toLowerCase().indexOf(q) !== -1;
        var inTags  = false;
        if (t.tags) {
          for (var i = 0; i < t.tags.length; i++) {
            if (t.tags[i].toLowerCase().indexOf(q) !== -1) { inTags = true; break; }
          }
        }
        if (!inTitle && !inDesc && !inTags) return false;
      }
      return true;
    });
  }

  // ── DOM builders ─────────────────────────────────────────────────────

  function buildAssigneeAvatar(assigneeId) {
    var member = getMemberById(assigneeId);
    if (!member) return '';
    var safeColor    = escHtml(member.color);
    var safeInitials = escHtml(member.initials);
    var safeName     = escHtml(member.name);
    return (
      '<div class="task-avatar" ' +
        'style="background:' + safeColor + ';" ' +
        'title="' + safeName + '">' +
        safeInitials +
      '</div>'
    );
  }

  function buildPriorityBadge(priority) {
    var cfg = PRIORITY_CONFIG[priority] || PRIORITY_CONFIG.medium;
    return (
      '<span class="priority-badge priority-badge--' + escHtml(priority) + '" ' +
        'style="background:' + cfg.bg + ';color:' + cfg.text + ';">' +
        '<span class="priority-dot" style="background:' + cfg.dot + ';"></span>' +
        cfg.label +
      '</span>'
    );
  }

  function buildDueDateChip(dueDateStr, status) {
    if (!dueDateStr) return '';
    var overdue = status !== 'done' && isOverdue(dueDateStr);
    var colorStyle = overdue
      ? 'color:#DC2626;font-weight:600;'
      : 'color:#94A3B8;';
    var icon = overdue
      ? '<svg width="10" height="10" viewBox="0 0 16 16" fill="currentColor" aria-hidden="true"><path d="M8 0a8 8 0 100 16A8 8 0 008 0zm.75 4.5v4.25l2.9 1.68-.62 1.07-3.28-1.9V4.5h1z"/></svg>'
      : '<svg width="10" height="10" viewBox="0 0 16 16" fill="currentColor" aria-hidden="true"><path d="M3.5 0a.5.5 0 01.5.5V1h8V.5a.5.5 0 011 0V1h1a2 2 0 012 2v11a2 2 0 01-2 2H2a2 2 0 01-2-2V3a2 2 0 012-2h1V.5a.5.5 0 01.5-.5zM1 4v10a1 1 0 001 1h12a1 1 0 001-1V4H1z"/></svg>';
    return (
      '<span class="task-due-date" style="' + colorStyle + '">' +
        icon + ' ' + escHtml(formatDate(dueDateStr)) +
      '</span>'
    );
  }

  function buildTagChips(tags) {
    if (!tags || tags.length === 0) return '';
    var visible = tags.slice(0, 2);
    var overflow = tags.length - 2;
    var html = '<div class="task-tags">';
    for (var i = 0; i < visible.length; i++) {
      html += '<span class="task-tag">' + escHtml(visible[i]) + '</span>';
    }
    if (overflow > 0) {
      html += '<span class="task-tag task-tag--more">+' + overflow + '</span>';
    }
    html += '</div>';
    return html;
  }

  function buildStoryPointsBadge(points) {
    if (!points || points <= 0) return '';
    return '<span class="task-story-points" title="Story points">' + escHtml(String(points)) + '</span>';
  }

  // ── Task card element ─────────────────────────────────────────────────

  function createTaskCard(task) {
    var card = document.createElement('div');
    card.className = 'task-card priority-' + task.priority;
    card.setAttribute('data-task-id', task.id);
    card.setAttribute('draggable', 'true');
    card.setAttribute('role', 'button');
    card.setAttribute('tabindex', '0');
    card.setAttribute('aria-label', escHtml(task.title));

    // ── Drag events ──
    card.addEventListener('dragstart', function (e) {
      e.dataTransfer.effectAllowed = 'move';
      e.dataTransfer.setData('text/plain', task.id);
      // Defer adding the class so the drag ghost renders the non-dimmed card
      var self = this;
      setTimeout(function () { self.classList.add('dragging'); }, 0);
    });

    card.addEventListener('dragend', function () {
      this.classList.remove('dragging');
    });

    // ── Click / keyboard open ──
    card.addEventListener('click', function (e) {
      e.stopPropagation();
      if (window.app && typeof window.app.openTaskModal === 'function') {
        window.app.openTaskModal(task.id);
      }
    });

    card.addEventListener('keydown', function (e) {
      if (e.key === 'Enter' || e.key === ' ') {
        e.preventDefault();
        if (window.app && typeof window.app.openTaskModal === 'function') {
          window.app.openTaskModal(task.id);
        }
      }
    });

    // ── Build inner HTML ──
    var overdue = task.status !== 'done' && isOverdue(task.due_date);
    if (overdue) card.classList.add('overdue');

    var headerHtml =
      '<div class="task-card__header">' +
        buildPriorityBadge(task.priority) +
        buildStoryPointsBadge(task.story_points) +
      '</div>';

    var titleHtml =
      '<div class="task-card__title">' + escHtml(task.title) + '</div>';

    var footerLeft =
      buildDueDateChip(task.due_date, task.status) +
      buildTagChips(task.tags);

    var footerRight =
      buildAssigneeAvatar(task.assignee_id);

    var footerHtml =
      '<div class="task-card__footer">' +
        '<div class="task-card__footer-left">' + footerLeft + '</div>' +
        '<div class="task-card__footer-right">' + footerRight + '</div>' +
      '</div>';

    card.innerHTML = headerHtml + titleHtml + footerHtml;
    return card;
  }

  // ── Column element ────────────────────────────────────────────────────

  function createColumn(colDef, tasks) {
    var col = document.createElement('div');
    col.className = 'board-column';
    col.setAttribute('data-status', colDef.status);

    // Header
    var header = document.createElement('div');
    header.className = 'board-column__header';
    header.innerHTML =
      '<div class="board-column__header-left">' +
        '<span class="board-column__dot" style="background:' + escHtml(colDef.color) + ';"></span>' +
        '<span class="board-column__label">' + escHtml(colDef.label) + '</span>' +
        '<span class="board-column__count" style="background:' + escHtml(colDef.color) + '1A;color:' + escHtml(colDef.color) + ';">' +
          tasks.length +
        '</span>' +
      '</div>';
    col.appendChild(header);

    // Scrollable body — this is the drop target
    var body = document.createElement('div');
    body.className = 'board-column__body';

    // Drag-over events on the body
    body.addEventListener('dragover', function (e) {
      e.preventDefault();
      e.dataTransfer.dropEffect = 'move';
      col.classList.add('drag-over');
    });

    body.addEventListener('dragleave', function (e) {
      // Only remove if we've left the column entirely (not moved into a child)
      if (!col.contains(e.relatedTarget)) {
        col.classList.remove('drag-over');
      }
    });

    body.addEventListener('drop', function (e) {
      e.preventDefault();
      col.classList.remove('drag-over');
      var taskId = e.dataTransfer.getData('text/plain');
      if (taskId) {
        window.store.moveTask(taskId, colDef.status);
        // store.moveTask emits 'task:moved' which triggers renderBoard via subscription
      }
    });

    // Task cards
    if (tasks.length === 0) {
      var empty = document.createElement('div');
      empty.className = 'board-column__empty';
      empty.textContent = 'No tasks';
      body.appendChild(empty);
    } else {
      for (var i = 0; i < tasks.length; i++) {
        body.appendChild(createTaskCard(tasks[i]));
      }
    }

    col.appendChild(body);

    // Add task button
    var addBtn = document.createElement('button');
    addBtn.className = 'board-column__add-btn';
    addBtn.setAttribute('type', 'button');
    addBtn.setAttribute('aria-label', 'Add task to ' + colDef.label);
    addBtn.innerHTML =
      '<svg width="14" height="14" viewBox="0 0 16 16" fill="currentColor" aria-hidden="true">' +
        '<path d="M8 0a1 1 0 011 1v6h6a1 1 0 010 2H9v6a1 1 0 01-2 0V9H1a1 1 0 010-2h6V1a1 1 0 011-1z"/>' +
      '</svg>' +
      ' Add task';

    var statusForClosure = colDef.status;
    addBtn.addEventListener('click', function () {
      if (window.app && typeof window.app.openNewTaskModal === 'function') {
        window.app.openNewTaskModal(statusForClosure);
      }
    });

    col.appendChild(addBtn);
    return col;
  }

  // ── Main render function ──────────────────────────────────────────────

  function renderBoard(filters) {
    // Persist active filters for re-renders triggered by store events
    if (filters !== undefined) {
      _currentFilters = filters || { project_id: null, assignee_id: null, priority: null, query: null };
    }

    var container = document.getElementById('board-container');
    if (!container) {
      console.warn('[board] #board-container not found — cannot render');
      return;
    }

    // Clear existing content
    container.innerHTML = '';

    // Build each column
    for (var i = 0; i < COLUMNS.length; i++) {
      var colDef = COLUMNS[i];

      // Get tasks for this column's status then apply the active filters
      var rawTasks = window.store.getTasksByStatus(colDef.status);
      var filteredTasks = applyFilters(rawTasks, _currentFilters);

      container.appendChild(createColumn(colDef, filteredTasks));
    }
  }

  // ── Store event subscriptions ─────────────────────────────────────────
  // These re-render the board while preserving whatever filters are active.

  window.store.on('task:added',   function () { renderBoard(); });
  window.store.on('task:updated', function () { renderBoard(); });
  window.store.on('task:moved',   function () { renderBoard(); });
  window.store.on('task:deleted', function () { renderBoard(); });

  // ── Expose globally ───────────────────────────────────────────────────
  window.board = {
    renderBoard: renderBoard
  };

})();
