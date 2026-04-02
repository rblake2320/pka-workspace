// FlowBoard Store — Single source of truth for Kanban project management
(function () {
  'use strict';

  var STORAGE_KEY = 'flowboard_data';
  var VALID_STATUSES = ['backlog', 'todo', 'in_progress', 'review', 'done'];
  var VALID_PRIORITIES = ['low', 'medium', 'high', 'critical'];

  // ── EventBus ──────────────────────────────────────────────────────────
  var _listeners = {};

  function on(event, cb) {
    if (typeof cb !== 'function') return;
    if (!_listeners[event]) _listeners[event] = [];
    _listeners[event].push(cb);
  }

  function off(event, cb) {
    if (!_listeners[event]) return;
    _listeners[event] = _listeners[event].filter(function (fn) { return fn !== cb; });
  }

  function emit(event, data) {
    if (!_listeners[event]) return;
    var cbs = _listeners[event].slice();
    for (var i = 0; i < cbs.length; i++) {
      try { cbs[i](data); } catch (_) { /* swallow listener errors */ }
    }
  }

  // ── ID generator ─────────────────────────────────────────────────────
  var _idCounter = Date.now();
  function nextId() {
    _idCounter += 1;
    return 'fb_' + _idCounter.toString(36);
  }

  // ── Date helpers ─────────────────────────────────────────────────────
  function today() { return new Date().toISOString().slice(0, 10); }

  function daysAgo(n) {
    var d = new Date();
    d.setDate(d.getDate() - n);
    return d.toISOString().slice(0, 10);
  }

  function daysFromNow(n) {
    var d = new Date();
    d.setDate(d.getDate() + n);
    return d.toISOString().slice(0, 10);
  }

  // ── Seed data ─────────────────────────────────────────────────────────

  function seedMembers() {
    return [
      { id: 'm1', name: 'Sarah Chen',      initials: 'SC', color: '#7C6BF2', role: 'Frontend Dev' },
      { id: 'm2', name: 'Marcus Johnson',   initials: 'MJ', color: '#F05A5A', role: 'Backend Dev' },
      { id: 'm3', name: 'Priya Patel',      initials: 'PP', color: '#22C55E', role: 'Designer' },
      { id: 'm4', name: 'David Kim',        initials: 'DK', color: '#F59E0B', role: 'QA' },
      { id: 'm5', name: 'Elena Vasquez',    initials: 'EV', color: '#06B6D4', role: 'PM' },
      { id: 'm6', name: 'James Okonkwo',    initials: 'JO', color: '#EC4899', role: 'DevOps' }
    ];
  }

  function seedProjects() {
    return [
      { id: 'p1', name: 'Website Redesign', color: '#7C6BF2', description: 'Complete overhaul of the company website with modern UI, improved accessibility, and performance optimizations.' },
      { id: 'p2', name: 'Mobile App',       color: '#22C55E', description: 'Native iOS and Android mobile application with offline support and push notifications.' },
      { id: 'p3', name: 'API v2',           color: '#F59E0B', description: 'Second major version of the public REST API with GraphQL support, rate limiting, and improved auth.' }
    ];
  }

  function seedTasks() {
    return [
      // ── Website Redesign (p1) ──────────────────────────────────────
      { id: 't01', title: 'Implement OAuth2 login flow',                     description: 'Add Google and GitHub OAuth2 providers with PKCE flow and token refresh.',                             status: 'done',        priority: 'high',     assignee_id: 'm1', project_id: 'p1', tags: ['auth', 'security'],        story_points: 8,  created_at: daysAgo(21), due_date: daysAgo(7),  completed_at: daysAgo(8) },
      { id: 't02', title: 'Design new landing page hero section',            description: 'Create high-fidelity mockup for the above-fold hero area with animated illustrations.',              status: 'done',        priority: 'high',     assignee_id: 'm3', project_id: 'p1', tags: ['design', 'landing'],       story_points: 5,  created_at: daysAgo(20), due_date: daysAgo(10), completed_at: daysAgo(6) },
      { id: 't03', title: 'Build responsive navigation component',           description: 'Hamburger menu on mobile, mega-menu on desktop. Keyboard accessible.',                              status: 'done',        priority: 'medium',   assignee_id: 'm1', project_id: 'p1', tags: ['ui', 'accessibility'],     story_points: 5,  created_at: daysAgo(18), due_date: daysAgo(5),  completed_at: daysAgo(5) },
      { id: 't04', title: 'Set up CI/CD pipeline for staging deploys',       description: 'GitHub Actions workflow: lint, test, build, deploy to staging on PR merge.',                         status: 'done',        priority: 'high',     assignee_id: 'm6', project_id: 'p1', tags: ['devops', 'ci'],            story_points: 5,  created_at: daysAgo(17), due_date: daysAgo(6),  completed_at: daysAgo(4) },
      { id: 't05', title: 'Optimize LCP for landing page below 2.5s',        description: 'Lazy load images, preconnect fonts, defer non-critical JS. Target LCP < 2.5s.',                    status: 'done',        priority: 'medium',   assignee_id: 'm1', project_id: 'p1', tags: ['performance'],             story_points: 3,  created_at: daysAgo(14), due_date: daysAgo(3),  completed_at: daysAgo(3) },
      { id: 't06', title: 'Write E2E tests for signup and login',            description: 'Playwright tests covering happy path, validation errors, OAuth redirect, and session persistence.',  status: 'done',        priority: 'medium',   assignee_id: 'm4', project_id: 'p1', tags: ['testing', 'e2e'],          story_points: 5,  created_at: daysAgo(13), due_date: daysAgo(2),  completed_at: daysAgo(2) },
      { id: 't07', title: 'Integrate Stripe subscription billing',           description: 'Monthly and annual plans, proration, webhook handling for payment events.',                         status: 'review',      priority: 'critical', assignee_id: 'm2', project_id: 'p1', tags: ['billing', 'integration'],  story_points: 13, created_at: daysAgo(15), due_date: daysFromNow(2) },
      { id: 't08', title: 'Implement dark mode toggle with persistence',     description: 'System preference detection, manual toggle, save to localStorage and user profile.',               status: 'review',      priority: 'low',      assignee_id: 'm1', project_id: 'p1', tags: ['ui', 'theme'],             story_points: 3,  created_at: daysAgo(10), due_date: daysFromNow(5) },
      { id: 't09', title: 'Build admin dashboard analytics widgets',         description: 'Revenue chart, user growth, churn rate, and active sessions. Use Recharts.',                        status: 'in_progress', priority: 'high',     assignee_id: 'm1', project_id: 'p1', tags: ['dashboard', 'analytics'],  story_points: 8,  created_at: daysAgo(8),  due_date: daysFromNow(3) },
      { id: 't10', title: 'Migrate user avatars to S3 with CloudFront CDN',  description: 'Move from local disk to S3. Serve via CloudFront. Handle migration of existing uploads.',          status: 'in_progress', priority: 'medium',   assignee_id: 'm6', project_id: 'p1', tags: ['devops', 'storage'],       story_points: 5,  created_at: daysAgo(7),  due_date: daysFromNow(4) },
      { id: 't11', title: 'Add WCAG 2.1 AA compliance to all forms',         description: 'Aria labels, focus management, error announcements, color contrast ratios.',                        status: 'in_progress', priority: 'high',     assignee_id: 'm3', project_id: 'p1', tags: ['accessibility', 'forms'],  story_points: 8,  created_at: daysAgo(6),  due_date: daysAgo(1) },
      { id: 't12', title: 'Implement real-time notifications with SSE',      description: 'Server-Sent Events for in-app notifications. Fallback to polling for older browsers.',              status: 'todo',        priority: 'medium',   assignee_id: 'm2', project_id: 'p1', tags: ['realtime', 'notifications'], story_points: 8, created_at: daysAgo(5),  due_date: daysFromNow(10) },
      { id: 't13', title: 'Create style guide and component library docs',   description: 'Storybook setup with all shared components documented with usage examples.',                        status: 'todo',        priority: 'low',      assignee_id: 'm3', project_id: 'p1', tags: ['docs', 'design-system'],   story_points: 5,  created_at: daysAgo(4),  due_date: daysFromNow(14) },
      { id: 't14', title: 'Add CSP headers and security audit fixes',        description: 'Content-Security-Policy headers, fix mixed content, remove inline scripts.',                        status: 'backlog',     priority: 'high',     assignee_id: 'm6', project_id: 'p1', tags: ['security'],                story_points: 5,  created_at: daysAgo(3),  due_date: daysFromNow(20) },
      { id: 't15', title: 'Implement lazy loading for dashboard modules',    description: 'Code-split dashboard widgets. Load only visible modules on initial render.',                         status: 'backlog',     priority: 'medium',   assignee_id: 'm1', project_id: 'p1', tags: ['performance'],             story_points: 5,  created_at: daysAgo(2),  due_date: daysFromNow(21) },

      // ── Mobile App (p2) ────────────────────────────────────────────
      { id: 't16', title: 'Set up React Native project with Expo',           description: 'Initialize project, configure TypeScript, ESLint, and Prettier. Set up navigation.',              status: 'done',        priority: 'high',     assignee_id: 'm1', project_id: 'p2', tags: ['setup', 'mobile'],         story_points: 3,  created_at: daysAgo(25), due_date: daysAgo(15), completed_at: daysAgo(9) },
      { id: 't17', title: 'Design onboarding flow mockups',                  description: 'Four-screen onboarding: welcome, features tour, permission requests, profile setup.',              status: 'done',        priority: 'high',     assignee_id: 'm3', project_id: 'p2', tags: ['design', 'onboarding'],    story_points: 5,  created_at: daysAgo(22), due_date: daysAgo(12), completed_at: daysAgo(7) },
      { id: 't18', title: 'Implement biometric authentication',              description: 'Face ID and fingerprint login using expo-local-authentication. Fallback to PIN.',                   status: 'done',        priority: 'critical', assignee_id: 'm2', project_id: 'p2', tags: ['auth', 'security', 'mobile'], story_points: 8, created_at: daysAgo(19), due_date: daysAgo(8), completed_at: daysAgo(1) },
      { id: 't19', title: 'Build offline-first data sync engine',            description: 'WatermelonDB for local storage, conflict resolution with server timestamps.',                       status: 'review',      priority: 'critical', assignee_id: 'm2', project_id: 'p2', tags: ['offline', 'sync'],          story_points: 13, created_at: daysAgo(16), due_date: daysFromNow(1) },
      { id: 't20', title: 'Create push notification service',                description: 'Firebase Cloud Messaging for Android, APNs for iOS. Topic subscriptions and deep links.',           status: 'in_progress', priority: 'high',     assignee_id: 'm6', project_id: 'p2', tags: ['notifications', 'mobile'], story_points: 8,  created_at: daysAgo(12), due_date: daysFromNow(5) },
      { id: 't21', title: 'Implement gesture-based task reordering',         description: 'Drag-and-drop with react-native-gesture-handler. Haptic feedback on drop.',                         status: 'in_progress', priority: 'medium',   assignee_id: 'm1', project_id: 'p2', tags: ['ui', 'gestures'],          story_points: 5,  created_at: daysAgo(9),  due_date: daysFromNow(6) },
      { id: 't22', title: 'Fix memory leak in websocket handler',            description: 'Connections not cleaned up on component unmount. Causing OOM on long sessions.',                     status: 'in_progress', priority: 'critical', assignee_id: 'm2', project_id: 'p2', tags: ['bug', 'performance'],      story_points: 5,  created_at: daysAgo(3),  due_date: daysAgo(1) },
      { id: 't23', title: 'Add pull-to-refresh on all list screens',         description: 'Consistent refresh UX with loading skeleton and error state handling.',                             status: 'todo',        priority: 'medium',   assignee_id: 'm1', project_id: 'p2', tags: ['ui', 'mobile'],            story_points: 3,  created_at: daysAgo(6),  due_date: daysFromNow(8) },
      { id: 't24', title: 'Write unit tests for sync conflict resolver',     description: 'Edge cases: simultaneous edits, delete-then-edit, offline queue overflow.',                          status: 'todo',        priority: 'high',     assignee_id: 'm4', project_id: 'p2', tags: ['testing', 'sync'],         story_points: 8,  created_at: daysAgo(5),  due_date: daysFromNow(7) },
      { id: 't25', title: 'Implement app-level error boundary',              description: 'Catch unhandled JS errors, show friendly recovery screen, report to Sentry.',                       status: 'todo',        priority: 'medium',   assignee_id: 'm1', project_id: 'p2', tags: ['error-handling'],          story_points: 3,  created_at: daysAgo(4),  due_date: daysFromNow(12) },
      { id: 't26', title: 'Design settings and profile screens',             description: 'User profile editing, notification preferences, theme selection, account deletion.',                 status: 'todo',        priority: 'low',      assignee_id: 'm3', project_id: 'p2', tags: ['design', 'mobile'],        story_points: 5,  created_at: daysAgo(3),  due_date: daysFromNow(15) },
      { id: 't27', title: 'Set up Fastlane for automated App Store builds',  description: 'Automated signing, build numbering, TestFlight uploads, and App Store screenshots.',               status: 'backlog',     priority: 'high',     assignee_id: 'm6', project_id: 'p2', tags: ['devops', 'mobile'],        story_points: 8,  created_at: daysAgo(2),  due_date: daysFromNow(18) },
      { id: 't28', title: 'Add app accessibility audit and VoiceOver support', description: 'Audit all screens for VoiceOver/TalkBack. Fix reading order and action labels.',                status: 'backlog',     priority: 'medium',   assignee_id: 'm3', project_id: 'p2', tags: ['accessibility', 'mobile'], story_points: 8,  created_at: daysAgo(1),  due_date: daysFromNow(22) },

      // ── API v2 (p3) ───────────────────────────────────────────────
      { id: 't29', title: 'Design API v2 schema and endpoint spec',          description: 'OpenAPI 3.1 spec with all endpoints, request/response schemas, and error codes.',                  status: 'done',        priority: 'critical', assignee_id: 'm5', project_id: 'p3', tags: ['api', 'design'],           story_points: 8,  created_at: daysAgo(28), due_date: daysAgo(18), completed_at: daysAgo(10) },
      { id: 't30', title: 'Implement rate limiting middleware',               description: 'Token bucket algorithm, per-user and per-IP limits, 429 responses with Retry-After header.',        status: 'done',        priority: 'high',     assignee_id: 'm2', project_id: 'p3', tags: ['api', 'security'],         story_points: 5,  created_at: daysAgo(24), due_date: daysAgo(14), completed_at: daysAgo(11) },
      { id: 't31', title: 'Add GraphQL layer with DataLoader batching',      description: 'Apollo Server setup, DataLoader for N+1 prevention, query depth limiting.',                        status: 'done',        priority: 'high',     assignee_id: 'm2', project_id: 'p3', tags: ['graphql', 'api'],          story_points: 13, created_at: daysAgo(20), due_date: daysAgo(8),  completed_at: daysAgo(3) },
      { id: 't32', title: 'Build API key management and rotation system',    description: 'Generate, revoke, and rotate API keys. Scoped permissions per key.',                               status: 'review',      priority: 'critical', assignee_id: 'm2', project_id: 'p3', tags: ['auth', 'api'],             story_points: 8,  created_at: daysAgo(14), due_date: daysFromNow(1) },
      { id: 't33', title: 'Implement request validation with Zod schemas',   description: 'Validate all incoming payloads, return structured 422 errors with field paths.',                    status: 'review',      priority: 'high',     assignee_id: 'm2', project_id: 'p3', tags: ['validation', 'api'],       story_points: 5,  created_at: daysAgo(10), due_date: daysFromNow(3) },
      { id: 't34', title: 'Set up API versioning with URL prefix strategy',  description: '/v1/* and /v2/* routing, shared middleware, deprecation headers on v1.',                             status: 'in_progress', priority: 'high',     assignee_id: 'm2', project_id: 'p3', tags: ['api', 'versioning'],       story_points: 5,  created_at: daysAgo(8),  due_date: daysFromNow(4) },
      { id: 't35', title: 'Write load test suite with k6',                   description: 'Simulate 1000 concurrent users, measure p95 latency, find bottlenecks.',                            status: 'in_progress', priority: 'medium',   assignee_id: 'm4', project_id: 'p3', tags: ['testing', 'performance'],  story_points: 5,  created_at: daysAgo(7),  due_date: daysFromNow(5) },
      { id: 't36', title: 'Add structured logging with correlation IDs',     description: 'JSON logs, request correlation ID header propagation, log aggregation setup.',                       status: 'todo',        priority: 'medium',   assignee_id: 'm6', project_id: 'p3', tags: ['observability', 'logging'], story_points: 5, created_at: daysAgo(5),  due_date: daysFromNow(9) },
      { id: 't37', title: 'Implement webhook delivery with retry logic',     description: 'POST to subscriber URLs, exponential backoff, dead letter queue after 5 failures.',                 status: 'todo',        priority: 'high',     assignee_id: 'm2', project_id: 'p3', tags: ['webhooks', 'api'],         story_points: 8,  created_at: daysAgo(4),  due_date: daysFromNow(11) },
      { id: 't38', title: 'Create SDK generator from OpenAPI spec',          description: 'Auto-generate TypeScript, Python, and Go client SDKs from the spec. Publish to npm/PyPI.',          status: 'todo',        priority: 'low',      assignee_id: 'm1', project_id: 'p3', tags: ['sdk', 'dx'],               story_points: 8,  created_at: daysAgo(3),  due_date: daysFromNow(20) },
      { id: 't39', title: 'Add database connection pooling with PgBouncer',  description: 'Configure PgBouncer in transaction mode, tune pool sizes for API worker count.',                     status: 'backlog',     priority: 'high',     assignee_id: 'm6', project_id: 'p3', tags: ['database', 'devops'],      story_points: 5,  created_at: daysAgo(2),  due_date: daysFromNow(16) },
      { id: 't40', title: 'Implement cursor-based pagination',               description: 'Replace offset pagination. Opaque cursors, consistent ordering, forward and backward support.',     status: 'backlog',     priority: 'medium',   assignee_id: 'm2', project_id: 'p3', tags: ['api', 'pagination'],       story_points: 5,  created_at: daysAgo(2),  due_date: daysFromNow(17) },
      { id: 't41', title: 'Write API migration guide for v1 consumers',      description: 'Document all breaking changes, provide code examples, and create a migration checklist.',            status: 'backlog',     priority: 'medium',   assignee_id: 'm5', project_id: 'p3', tags: ['docs', 'api'],             story_points: 3,  created_at: daysAgo(1),  due_date: daysFromNow(25) },
      { id: 't42', title: 'Add OpenTelemetry distributed tracing',           description: 'Instrument all API routes, propagate trace context, export to Jaeger.',                              status: 'backlog',     priority: 'low',      assignee_id: 'm6', project_id: 'p3', tags: ['observability', 'tracing'], story_points: 8, created_at: daysAgo(1),  due_date: daysFromNow(28) },
      { id: 't43', title: 'Security penetration test on auth endpoints',     description: 'OWASP Top 10 checks, brute force protection, JWT tampering, SQL injection on search.',              status: 'todo',        priority: 'critical', assignee_id: 'm4', project_id: 'p3', tags: ['security', 'testing'],     story_points: 8,  created_at: daysAgo(6),  due_date: daysFromNow(6) },
      { id: 't44', title: 'Implement idempotency keys for POST endpoints',   description: 'Accept Idempotency-Key header, store results for 24h, return cached response on replay.',           status: 'todo',        priority: 'medium',   assignee_id: 'm2', project_id: 'p3', tags: ['api', 'reliability'],      story_points: 5,  created_at: daysAgo(4),  due_date: daysFromNow(13) }
    ];
  }

  // ── Core store object ────────────────────────────────────────────────

  var store = {
    tasks: [],
    members: [],
    projects: [],

    // EventBus
    on: on,
    off: off,
    emit: emit,

    // ── Query methods ──────────────────────────────────────────────────

    getTasksByStatus: function (status) {
      return store.tasks.filter(function (t) { return t.status === status; });
    },

    getTasksByAssignee: function (memberId) {
      return store.tasks.filter(function (t) { return t.assignee_id === memberId; });
    },

    getTasksByProject: function (projectId) {
      return store.tasks.filter(function (t) { return t.project_id === projectId; });
    },

    // ── Mutation methods ───────────────────────────────────────────────

    addTask: function (taskData) {
      var task = {
        id:          taskData.id || nextId(),
        title:       taskData.title || 'Untitled task',
        description: taskData.description || '',
        status:      VALID_STATUSES.indexOf(taskData.status) !== -1 ? taskData.status : 'backlog',
        priority:    VALID_PRIORITIES.indexOf(taskData.priority) !== -1 ? taskData.priority : 'medium',
        assignee_id: taskData.assignee_id || null,
        project_id:  taskData.project_id || null,
        tags:        Array.isArray(taskData.tags) ? taskData.tags.slice() : [],
        story_points: typeof taskData.story_points === 'number' ? taskData.story_points : 0,
        created_at:  taskData.created_at || today(),
        due_date:    taskData.due_date || null,
        completed_at: taskData.completed_at || null
      };
      store.tasks.push(task);
      _autoSave();
      emit('task:added', task);
      return task;
    },

    updateTask: function (id, changes) {
      var task = _findTask(id);
      if (!task) return null;

      var keys = Object.keys(changes);
      for (var i = 0; i < keys.length; i++) {
        var key = keys[i];
        if (key === 'id') continue; // immutable
        if (key === 'status' && VALID_STATUSES.indexOf(changes[key]) === -1) continue;
        if (key === 'priority' && VALID_PRIORITIES.indexOf(changes[key]) === -1) continue;
        if (key === 'tags') {
          task.tags = Array.isArray(changes.tags) ? changes.tags.slice() : task.tags;
          continue;
        }
        task[key] = changes[key];
      }

      // Track completion timestamp
      if (changes.status === 'done' && !task.completed_at) {
        task.completed_at = today();
      }
      if (changes.status && changes.status !== 'done') {
        task.completed_at = null;
      }

      _autoSave();
      emit('task:updated', task);
      return task;
    },

    deleteTask: function (id) {
      var idx = _findTaskIndex(id);
      if (idx === -1) return;
      var removed = store.tasks.splice(idx, 1)[0];
      _autoSave();
      emit('task:deleted', removed);
    },

    moveTask: function (id, newStatus) {
      if (VALID_STATUSES.indexOf(newStatus) === -1) return null;
      var task = _findTask(id);
      if (!task) return null;

      var oldStatus = task.status;
      task.status = newStatus;

      if (newStatus === 'done' && !task.completed_at) {
        task.completed_at = today();
      }
      if (newStatus !== 'done') {
        task.completed_at = null;
      }

      _autoSave();
      emit('task:moved', { task: task, from: oldStatus, to: newStatus });
      return task;
    },

    // ── Filter and search ──────────────────────────────────────────────

    filterTasks: function (filters) {
      if (!filters || typeof filters !== 'object') return store.tasks.slice();

      return store.tasks.filter(function (t) {
        if (filters.status && t.status !== filters.status) return false;
        if (filters.priority && t.priority !== filters.priority) return false;
        if (filters.assignee && t.assignee_id !== filters.assignee) return false;
        if (filters.assignee_id && t.assignee_id !== filters.assignee_id) return false;
        if (filters.project && t.project_id !== filters.project) return false;
        if (filters.project_id && t.project_id !== filters.project_id) return false;
        return true;
      });
    },

    searchTasks: function (query) {
      if (!query || typeof query !== 'string') return [];
      var q = query.toLowerCase();
      return store.tasks.filter(function (t) {
        if (t.title && t.title.toLowerCase().indexOf(q) !== -1) return true;
        if (t.description && t.description.toLowerCase().indexOf(q) !== -1) return true;
        if (t.tags) {
          for (var i = 0; i < t.tags.length; i++) {
            if (t.tags[i].toLowerCase().indexOf(q) !== -1) return true;
          }
        }
        return false;
      });
    },

    // ── Stats ──────────────────────────────────────────────────────────

    getStats: function () {
      var tasks = store.tasks;
      var total = tasks.length;

      // By status
      var byStatus = { backlog: 0, todo: 0, in_progress: 0, review: 0, done: 0 };
      for (var i = 0; i < tasks.length; i++) {
        if (byStatus.hasOwnProperty(tasks[i].status)) {
          byStatus[tasks[i].status]++;
        }
      }

      // By priority
      var byPriority = { low: 0, medium: 0, high: 0, critical: 0 };
      for (var j = 0; j < tasks.length; j++) {
        if (byPriority.hasOwnProperty(tasks[j].priority)) {
          byPriority[tasks[j].priority]++;
        }
      }

      // Completion rate
      var completionRate = total > 0 ? byStatus.done / total : 0;

      // Overdue count: tasks not done with due_date in the past
      var todayStr = today();
      var overdueCount = 0;
      for (var k = 0; k < tasks.length; k++) {
        if (tasks[k].status !== 'done' && tasks[k].due_date && tasks[k].due_date < todayStr) {
          overdueCount++;
        }
      }

      // Velocity last 7 days: tasks completed each day
      var velocityLast7Days = _computeVelocity(7);

      // Burndown last 14 days
      var burndown = _computeBurndown(14);

      return {
        total: total,
        byStatus: byStatus,
        byPriority: byPriority,
        velocityLast7Days: velocityLast7Days,
        completionRate: Math.round(completionRate * 1000) / 1000,
        overdueCount: overdueCount,
        burndown: burndown
      };
    },

    // ── Persistence ────────────────────────────────────────────────────

    saveToStorage: function () {
      try {
        var data = {
          tasks: store.tasks,
          members: store.members,
          projects: store.projects,
          savedAt: new Date().toISOString()
        };
        localStorage.setItem(STORAGE_KEY, JSON.stringify(data));
      } catch (_) { /* localStorage full or unavailable */ }
    },

    loadFromStorage: function () {
      var loaded = false;
      try {
        var raw = localStorage.getItem(STORAGE_KEY);
        if (raw) {
          var data = JSON.parse(raw);
          if (data && Array.isArray(data.tasks) && data.tasks.length > 0) {
            store.tasks = data.tasks;
            store.members = Array.isArray(data.members) && data.members.length > 0 ? data.members : seedMembers();
            store.projects = Array.isArray(data.projects) && data.projects.length > 0 ? data.projects : seedProjects();
            loaded = true;
          }
        }
      } catch (_) { /* corrupt data, fall through to seed */ }

      if (!loaded) {
        store.members = seedMembers();
        store.projects = seedProjects();
        store.tasks = [];
        var seeds = seedTasks();
        for (var i = 0; i < seeds.length; i++) {
          store.tasks.push(seeds[i]);
        }
        store.saveToStorage();
      }

      emit('store:ready', {
        tasks: store.tasks.length,
        members: store.members.length,
        projects: store.projects.length
      });
    }
  };

  // ── Internal helpers ─────────────────────────────────────────────────

  function _findTask(id) {
    for (var i = 0; i < store.tasks.length; i++) {
      if (store.tasks[i].id === id) return store.tasks[i];
    }
    return null;
  }

  function _findTaskIndex(id) {
    for (var i = 0; i < store.tasks.length; i++) {
      if (store.tasks[i].id === id) return i;
    }
    return -1;
  }

  function _autoSave() {
    store.saveToStorage();
  }

  function _computeVelocity(days) {
    var velocity = [];
    for (var d = days - 1; d >= 0; d--) {
      var dateStr = daysAgo(d);
      var count = 0;
      for (var i = 0; i < store.tasks.length; i++) {
        if (store.tasks[i].completed_at === dateStr) {
          count++;
        }
      }
      velocity.push(count);
    }
    return velocity;
  }

  function _computeBurndown(days) {
    var burndown = [];
    // Total non-done tasks that existed on each date
    for (var d = days - 1; d >= 0; d--) {
      var dateStr = daysAgo(d);
      var remaining = 0;
      for (var i = 0; i < store.tasks.length; i++) {
        var t = store.tasks[i];
        // Task existed on this date if created_at <= dateStr
        if (t.created_at && t.created_at <= dateStr) {
          // Task was still open on this date if it was not yet completed,
          // or was completed after this date
          if (!t.completed_at || t.completed_at > dateStr) {
            remaining++;
          }
        }
      }
      burndown.push({ date: dateStr, remaining: remaining });
    }
    return burndown;
  }

  // ── Expose globally ──────────────────────────────────────────────────
  window.store = store;
})();
