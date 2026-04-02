// FlowBoard App Controller — Bootstraps and wires the entire application
(function () {
  'use strict';

  // ── Priority / Status display maps ───────────────────────────────────────
  var PRIORITY_CONFIG = {
    critical: { label: 'Critical', bg: '#FEE2E2', text: '#DC2626', dot: '#DC2626' },
    high:     { label: 'High',     bg: '#FEF3C7', text: '#D97706', dot: '#F59E0B' },
    medium:   { label: 'Medium',   bg: '#DBEAFE', text: '#1D4ED8', dot: '#3B82F6' },
    low:      { label: 'Low',      bg: '#F1F5F9', text: '#64748B', dot: '#94A3B8' }
  };

  var STATUS_LABELS = {
    backlog:     'Backlog',
    todo:        'To Do',
    in_progress: 'In Progress',
    review:      'Review',
    done:        'Done'
  };

  // ── Active filter state ──────────────────────────────────────────────────
  var currentFilters = {
    project_id:  null,
    assignee_id: null,
    priority:    null,
    query:       null
  };

  // ── Currently active view ────────────────────────────────────────────────
  var currentView = 'board';   // 'board' | 'list' | 'analytics'

  // ── Task being edited in the modal ──────────────────────────────────────
  var _editingTaskId = null;

  // ── HTML-escape helper ───────────────────────────────────────────────────
  function esc(str) {
    if (str == null) return '';
    return String(str)
      .replace(/&/g, '&amp;')
      .replace(/</g, '&lt;')
      .replace(/>/g, '&gt;')
      .replace(/"/g, '&quot;')
      .replace(/'/g, '&#39;');
  }

  // ── Date helpers ─────────────────────────────────────────────────────────
  function formatDate(dateStr) {
    if (!dateStr) return '';
    var parts = dateStr.split('-');
    if (parts.length !== 3) return dateStr;
    var d = new Date(
      parseInt(parts[0], 10),
      parseInt(parts[1], 10) - 1,
      parseInt(parts[2], 10)
    );
    return d.toLocaleDateString(undefined, { month: 'short', day: 'numeric' });
  }

  function isOverdue(dueDateStr, status) {
    if (!dueDateStr || status === 'done') return false;
    var today = new Date().toISOString().slice(0, 10);
    return dueDateStr < today;
  }

  // ── Member / project lookups ─────────────────────────────────────────────
  function getMemberById(id) {
    var members = window.store.members;
    for (var i = 0; i < members.length; i++) {
      if (members[i].id === id) return members[i];
    }
    return null;
  }

  function getProjectById(id) {
    var projects = window.store.projects;
    for (var i = 0; i < projects.length; i++) {
      if (projects[i].id === id) return projects[i];
    }
    return null;
  }

  // ── updateStats ──────────────────────────────────────────────────────────
  function updateStats() {
    var stats = window.store.getStats();

    var elTotal      = document.getElementById('stats-total');
    var elInProgress = document.getElementById('stats-inprogress');
    var elDone       = document.getElementById('stats-done');
    var elOverdue    = document.getElementById('stats-overdue');

    if (elTotal)      elTotal.textContent      = stats.total;
    if (elInProgress) elInProgress.textContent = stats.byStatus.in_progress;
    if (elDone)       elDone.textContent        = stats.byStatus.done;
    if (elOverdue)    elOverdue.textContent     = stats.overdueCount;
  }

  // ── Sidebar project list ─────────────────────────────────────────────────
  function renderSidebarProjects() {
    var container = document.getElementById('project-list');
    if (!container) return;

    // "All Projects" entry
    var allDiv = document.createElement('div');
    allDiv.className = 'sidebar-project' + (currentFilters.project_id === null ? ' active' : '');
    allDiv.innerHTML =
      '<span class="sidebar-project__dot" style="background:#7C6BF2;"></span>' +
      '<span class="sidebar-project__name">All Projects</span>' +
      '<span class="sidebar-project__count">' + window.store.tasks.length + '</span>';
    allDiv.addEventListener('click', function () {
      currentFilters.project_id = null;
      updateViewTitle(null);
      renderSidebarProjects();
      rerenderCurrentView();
    });
    container.innerHTML = '';
    container.appendChild(allDiv);

    var projects = window.store.projects;
    for (var i = 0; i < projects.length; i++) {
      (function (project) {
        var count = 0;
        var tasks = window.store.tasks;
        for (var j = 0; j < tasks.length; j++) {
          if (tasks[j].project_id === project.id) count++;
        }

        var div = document.createElement('div');
        div.className = 'sidebar-project' + (currentFilters.project_id === project.id ? ' active' : '');
        div.innerHTML =
          '<span class="sidebar-project__dot" style="background:' + esc(project.color) + ';"></span>' +
          '<span class="sidebar-project__name">' + esc(project.name) + '</span>' +
          '<span class="sidebar-project__count">' + count + '</span>';
        div.addEventListener('click', function () {
          currentFilters.project_id = project.id;
          updateViewTitle(project.name);
          renderSidebarProjects();
          rerenderCurrentView();
        });
        container.appendChild(div);
      })(projects[i]);
    }
  }

  // ── Sidebar member list ──────────────────────────────────────────────────
  function renderSidebarMembers() {
    var container = document.getElementById('member-list');
    if (!container) return;
    container.innerHTML = '';

    // "All members" reset entry
    var allDiv = document.createElement('div');
    allDiv.className = 'sidebar-member' + (currentFilters.assignee_id === null ? ' active' : '');
    allDiv.innerHTML =
      '<div class="sidebar-member__avatar" style="background:#334155;">AL</div>' +
      '<span class="sidebar-member__name">All Members</span>';
    allDiv.addEventListener('click', function () {
      currentFilters.assignee_id = null;
      renderSidebarMembers();
      rerenderCurrentView();
    });
    container.appendChild(allDiv);

    var members = window.store.members;
    for (var i = 0; i < members.length; i++) {
      (function (member) {
        var div = document.createElement('div');
        div.className = 'sidebar-member' + (currentFilters.assignee_id === member.id ? ' active' : '');
        div.innerHTML =
          '<div class="sidebar-member__avatar" style="background:' + esc(member.color) + ';">' +
            esc(member.initials) +
          '</div>' +
          '<span class="sidebar-member__name">' + esc(member.name) + '</span>';
        div.addEventListener('click', function () {
          currentFilters.assignee_id = member.id;
          renderSidebarMembers();
          rerenderCurrentView();
        });
        container.appendChild(div);
      })(members[i]);
    }
  }

  // ── Populate modal selects ───────────────────────────────────────────────
  function populateModalSelects() {
    var assigneeSelect = document.getElementById('modal-assignee');
    var projectSelect  = document.getElementById('modal-project');

    if (assigneeSelect) {
      assigneeSelect.innerHTML = '<option value="">Unassigned</option>';
      var members = window.store.members;
      for (var i = 0; i < members.length; i++) {
        var opt = document.createElement('option');
        opt.value = members[i].id;
        opt.textContent = members[i].name;
        assigneeSelect.appendChild(opt);
      }
    }

    if (projectSelect) {
      projectSelect.innerHTML = '<option value="">No Project</option>';
      var projects = window.store.projects;
      for (var j = 0; j < projects.length; j++) {
        var popt = document.createElement('option');
        popt.value = projects[j].id;
        popt.textContent = projects[j].name;
        projectSelect.appendChild(popt);
      }
    }
  }

  // ── View title ────────────────────────────────────────────────────────────
  function updateViewTitle(projectName) {
    var el = document.getElementById('view-title');
    if (el) el.textContent = projectName || 'All Projects';
  }

  // ── Re-render whichever view is currently active ──────────────────────────
  function rerenderCurrentView() {
    if (currentView === 'board') {
      window.board.renderBoard(currentFilters);
    } else if (currentView === 'list') {
      renderListView(currentFilters);
    } else if (currentView === 'analytics') {
      window.analytics.renderAnalytics();
    }
  }

  // ── View switching ────────────────────────────────────────────────────────
  function switchView(viewName) {
    currentView = viewName;

    var views = ['board', 'list', 'analytics'];
    for (var i = 0; i < views.length; i++) {
      var el = document.getElementById('view-' + views[i]);
      if (el) {
        if (views[i] === viewName) {
          el.classList.remove('hidden');
        } else {
          el.classList.add('hidden');
        }
      }
    }

    var navBtns = document.querySelectorAll('.nav-btn[data-view]');
    for (var j = 0; j < navBtns.length; j++) {
      if (navBtns[j].getAttribute('data-view') === viewName) {
        navBtns[j].classList.add('active');
      } else {
        navBtns[j].classList.remove('active');
      }
    }

    if (viewName === 'analytics') {
      window.analytics.renderAnalytics();
    } else if (viewName === 'list') {
      renderListView(currentFilters);
    }
  }

  // ── List view ─────────────────────────────────────────────────────────────
  function applyLocalFilters(tasks, filters) {
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
          for (var k = 0; k < t.tags.length; k++) {
            if (t.tags[k].toLowerCase().indexOf(q) !== -1) { inTags = true; break; }
          }
        }
        if (!inTitle && !inDesc && !inTags) return false;
      }
      return true;
    });
  }

  function renderListView(filters) {
    var container = document.getElementById('list-container');
    if (!container) return;

    var tasks = applyLocalFilters(window.store.tasks.slice(), filters || currentFilters);

    // Sort by due_date ascending; tasks with no due date go to end
    tasks.sort(function (a, b) {
      if (!a.due_date && !b.due_date) return 0;
      if (!a.due_date) return 1;
      if (!b.due_date) return -1;
      return a.due_date < b.due_date ? -1 : a.due_date > b.due_date ? 1 : 0;
    });

    if (tasks.length === 0) {
      container.innerHTML =
        '<div class="list-empty">No tasks match the current filters.</div>';
      return;
    }

    var html =
      '<table class="list-table">' +
        '<thead>' +
          '<tr>' +
            '<th class="list-th">Title</th>' +
            '<th class="list-th">Priority</th>' +
            '<th class="list-th">Status</th>' +
            '<th class="list-th">Assignee</th>' +
            '<th class="list-th">Project</th>' +
            '<th class="list-th">Due Date</th>' +
            '<th class="list-th list-th--center">Pts</th>' +
          '</tr>' +
        '</thead>' +
        '<tbody>';

    for (var i = 0; i < tasks.length; i++) {
      var task = tasks[i];
      var pcfg  = PRIORITY_CONFIG[task.priority] || PRIORITY_CONFIG.medium;
      var member  = getMemberById(task.assignee_id);
      var project = getProjectById(task.project_id);
      var overdue = isOverdue(task.due_date, task.status);

      var priorityBadge =
        '<span class="list-priority-badge" style="background:' + pcfg.bg + ';color:' + pcfg.text + ';">' +
          '<span style="display:inline-block;width:6px;height:6px;border-radius:50%;background:' + pcfg.dot + ';margin-right:4px;vertical-align:middle;"></span>' +
          esc(pcfg.label) +
        '</span>';

      var statusLabel = STATUS_LABELS[task.status] || task.status;
      var statusBadge =
        '<span class="list-status-badge list-status-badge--' + esc(task.status) + '">' +
          esc(statusLabel) +
        '</span>';

      var avatarHtml = member
        ? '<div class="list-avatar" style="background:' + esc(member.color) + ';" title="' + esc(member.name) + '">' +
            esc(member.initials) +
          '</div> ' + esc(member.name)
        : '<span class="list-unassigned">—</span>';

      var projectHtml = project
        ? '<span class="list-project-dot" style="background:' + esc(project.color) + ';"></span>' + esc(project.name)
        : '<span class="list-unassigned">—</span>';

      var dueDateHtml = task.due_date
        ? '<span class="' + (overdue ? 'list-due-overdue' : 'list-due') + '">' +
            esc(formatDate(task.due_date)) +
          '</span>'
        : '<span class="list-unassigned">—</span>';

      html +=
        '<tr class="list-row" data-task-id="' + esc(task.id) + '">' +
          '<td class="list-td list-td--title">' + esc(task.title) + '</td>' +
          '<td class="list-td">' + priorityBadge + '</td>' +
          '<td class="list-td">' + statusBadge + '</td>' +
          '<td class="list-td list-td--assignee">' + avatarHtml + '</td>' +
          '<td class="list-td list-td--project">' + projectHtml + '</td>' +
          '<td class="list-td">' + dueDateHtml + '</td>' +
          '<td class="list-td list-td--center">' +
            (task.story_points ? esc(String(task.story_points)) : '—') +
          '</td>' +
        '</tr>';
    }

    html += '</tbody></table>';
    container.innerHTML = html;

    // Wire row clicks
    var rows = container.querySelectorAll('.list-row');
    for (var r = 0; r < rows.length; r++) {
      (function (row) {
        row.addEventListener('click', function () {
          openTaskModal(row.getAttribute('data-task-id'));
        });
      })(rows[r]);
    }
  }

  // ── Modal: open for editing ───────────────────────────────────────────────
  function openTaskModal(taskId) {
    var overlay = document.getElementById('task-modal-overlay');
    if (!overlay) return;

    var task = null;
    var tasks = window.store.tasks;
    for (var i = 0; i < tasks.length; i++) {
      if (tasks[i].id === taskId) { task = tasks[i]; break; }
    }
    if (!task) return;

    _editingTaskId = taskId;

    _setModalField('modal-title',        task.title        || '');
    _setModalField('modal-description',  task.description  || '');
    _setModalField('modal-status',       task.status       || 'backlog');
    _setModalField('modal-priority',     task.priority     || 'medium');
    _setModalField('modal-assignee',     task.assignee_id  || '');
    _setModalField('modal-project',      task.project_id   || '');
    _setModalField('modal-due-date',     task.due_date     || '');
    _setModalField('modal-story-points', task.story_points != null ? String(task.story_points) : '');
    _setModalField('modal-tags',         Array.isArray(task.tags) ? task.tags.join(', ') : '');

    var heading = document.getElementById('modal-heading');
    if (heading) heading.textContent = 'Edit Task';

    var deleteBtn = document.getElementById('btn-modal-delete');
    if (deleteBtn) deleteBtn.classList.remove('hidden');

    overlay.classList.remove('hidden');

    var titleInput = document.getElementById('modal-title');
    if (titleInput) titleInput.focus();
  }

  // ── Modal: open for new task ──────────────────────────────────────────────
  function openNewTaskModal(defaultStatus) {
    var overlay = document.getElementById('task-modal-overlay');
    if (!overlay) return;

    _editingTaskId = null;

    _setModalField('modal-title',        '');
    _setModalField('modal-description',  '');
    _setModalField('modal-status',       defaultStatus || 'todo');
    _setModalField('modal-priority',     'medium');
    _setModalField('modal-assignee',     '');
    _setModalField('modal-project',      currentFilters.project_id || '');
    _setModalField('modal-due-date',     '');
    _setModalField('modal-story-points', '');
    _setModalField('modal-tags',         '');

    var heading = document.getElementById('modal-heading');
    if (heading) heading.textContent = 'New Task';

    var deleteBtn = document.getElementById('btn-modal-delete');
    if (deleteBtn) deleteBtn.classList.add('hidden');

    overlay.classList.remove('hidden');

    var titleInput = document.getElementById('modal-title');
    if (titleInput) titleInput.focus();
  }

  // ── Modal: close ─────────────────────────────────────────────────────────
  function closeModal() {
    var overlay = document.getElementById('task-modal-overlay');
    if (overlay) overlay.classList.add('hidden');
    _editingTaskId = null;
  }

  // ── Modal: save ──────────────────────────────────────────────────────────
  function _handleSave() {
    var titleInput = document.getElementById('modal-title');
    var title = titleInput ? titleInput.value.trim() : '';

    if (!title) {
      if (titleInput) {
        titleInput.classList.add('shake');
        titleInput.focus();
        setTimeout(function () { titleInput.classList.remove('shake'); }, 500);
      }
      return;
    }

    var tagsRaw = _getModalField('modal-tags');
    var tags = tagsRaw
      ? tagsRaw.split(',').map(function (t) { return t.trim(); }).filter(function (t) { return t.length > 0; })
      : [];

    var pointsRaw = _getModalField('modal-story-points');
    var points = pointsRaw ? parseInt(pointsRaw, 10) : 0;
    if (isNaN(points) || points < 0) points = 0;

    var changes = {
      title:        title,
      description:  _getModalField('modal-description'),
      status:       _getModalField('modal-status'),
      priority:     _getModalField('modal-priority'),
      assignee_id:  _getModalField('modal-assignee')  || null,
      project_id:   _getModalField('modal-project')   || null,
      due_date:     _getModalField('modal-due-date')   || null,
      story_points: points,
      tags:         tags
    };

    if (_editingTaskId) {
      window.store.updateTask(_editingTaskId, changes);
    } else {
      window.store.addTask(changes);
    }

    closeModal();
    updateStats();
    renderSidebarProjects();

    if (currentView === 'board') {
      window.board.renderBoard(currentFilters);
    } else if (currentView === 'list') {
      renderListView(currentFilters);
    }
  }

  // ── Modal: delete ─────────────────────────────────────────────────────────
  function _handleDelete() {
    if (!_editingTaskId) return;
    if (!window.confirm('Delete this task?')) return;
    window.store.deleteTask(_editingTaskId);
    closeModal();
    updateStats();
    renderSidebarProjects();
    window.board.renderBoard(currentFilters);
  }

  // ── Modal field helpers ───────────────────────────────────────────────────
  function _setModalField(id, value) {
    var el = document.getElementById(id);
    if (!el) return;
    el.value = value;
  }

  function _getModalField(id) {
    var el = document.getElementById(id);
    return el ? el.value : '';
  }

  // ── Wire all event listeners ──────────────────────────────────────────────
  function wireEvents() {
    // Nav buttons
    var navBtns = document.querySelectorAll('.nav-btn[data-view]');
    for (var i = 0; i < navBtns.length; i++) {
      (function (btn) {
        btn.addEventListener('click', function () {
          switchView(btn.getAttribute('data-view'));
        });
      })(navBtns[i]);
    }

    // New task button
    var btnNewTask = document.getElementById('btn-new-task');
    if (btnNewTask) {
      btnNewTask.addEventListener('click', function () {
        openNewTaskModal('todo');
      });
    }

    // Search
    var searchInput = document.getElementById('search-input');
    if (searchInput) {
      searchInput.addEventListener('input', function () {
        var q = searchInput.value.trim();
        currentFilters.query = q.length > 0 ? q : null;
        rerenderCurrentView();
      });
    }

    // Priority filter
    var filterPriority = document.getElementById('filter-priority');
    if (filterPriority) {
      filterPriority.addEventListener('change', function () {
        var val = filterPriority.value;
        currentFilters.priority = val && val !== '' ? val : null;
        rerenderCurrentView();
      });
    }

    // Modal save
    var btnSave = document.getElementById('btn-modal-save');
    if (btnSave) {
      btnSave.addEventListener('click', _handleSave);
    }

    // Modal cancel
    var btnCancel = document.getElementById('btn-modal-cancel');
    if (btnCancel) {
      btnCancel.addEventListener('click', closeModal);
    }

    // Modal close (X)
    var btnClose = document.getElementById('btn-modal-close');
    if (btnClose) {
      btnClose.addEventListener('click', closeModal);
    }

    // Modal delete
    var btnDelete = document.getElementById('btn-modal-delete');
    if (btnDelete) {
      btnDelete.addEventListener('click', _handleDelete);
    }

    // Close modal on overlay click (outside the modal box itself)
    var overlay = document.getElementById('task-modal-overlay');
    if (overlay) {
      overlay.addEventListener('click', function (e) {
        if (e.target === overlay) closeModal();
      });
    }

    // Close modal on Escape key
    document.addEventListener('keydown', function (e) {
      if (e.key === 'Escape') {
        var ov = document.getElementById('task-modal-overlay');
        if (ov && !ov.classList.contains('hidden')) closeModal();
      }
    });

    // Modal: submit on Enter in title field
    var titleInput = document.getElementById('modal-title');
    if (titleInput) {
      titleInput.addEventListener('keydown', function (e) {
        if (e.key === 'Enter') {
          e.preventDefault();
          _handleSave();
        }
      });
    }
  }

  // ── Store event subscriptions ─────────────────────────────────────────────
  function wireStoreEvents() {
    window.store.on('task:added',   function () { updateStats(); renderSidebarProjects(); });
    window.store.on('task:updated', function () { updateStats(); renderSidebarProjects(); });
    window.store.on('task:moved',   function () { updateStats(); renderSidebarProjects(); });
    window.store.on('task:deleted', function () { updateStats(); renderSidebarProjects(); });
  }

  // ── Bootstrap ─────────────────────────────────────────────────────────────
  function init() {
    // 1. Load from storage (seeds if empty)
    window.store.loadFromStorage();

    // 2. Render sidebar
    renderSidebarProjects();
    renderSidebarMembers();

    // 3. Populate modal selects
    populateModalSelects();

    // 4. Initial board render
    window.board.renderBoard(currentFilters);

    // 5. Update stats
    updateStats();

    // 6. Wire UI events
    wireEvents();

    // 7. Wire store events
    wireStoreEvents();

    // 8. Activate the board nav button
    var boardBtn = document.querySelector('.nav-btn[data-view="board"]');
    if (boardBtn) boardBtn.classList.add('active');
  }

  // ── Public API ────────────────────────────────────────────────────────────
  window.app = {
    openTaskModal:    openTaskModal,
    openNewTaskModal: openNewTaskModal,
    closeModal:       closeModal,
    updateStats:      updateStats
  };

  // ── Start ─────────────────────────────────────────────────────────────────
  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', init);
  } else {
    init();
  }

})();
