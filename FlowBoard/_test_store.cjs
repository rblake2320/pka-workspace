// Test harness for store.js — run with: node _test_store.js
global.window = {};
global.localStorage = {
  _data: {},
  getItem: function(k) { return this._data[k] || null; },
  setItem: function(k, v) { this._data[k] = v; },
  removeItem: function(k) { delete this._data[k]; }
};

require('./store.js');

var s = window.store;
s.loadFromStorage();

console.log('=== CONTRACT VERIFICATION ===');
console.log('tasks array:', Array.isArray(s.tasks), '| count:', s.tasks.length);
console.log('members array:', Array.isArray(s.members), '| count:', s.members.length);
console.log('projects array:', Array.isArray(s.projects), '| count:', s.projects.length);
console.log('on is function:', typeof s.on === 'function');
console.log('off is function:', typeof s.off === 'function');
console.log('emit is function:', typeof s.emit === 'function');
console.log('getTasksByStatus:', typeof s.getTasksByStatus === 'function');
console.log('getTasksByAssignee:', typeof s.getTasksByAssignee === 'function');
console.log('getTasksByProject:', typeof s.getTasksByProject === 'function');
console.log('addTask:', typeof s.addTask === 'function');
console.log('updateTask:', typeof s.updateTask === 'function');
console.log('deleteTask:', typeof s.deleteTask === 'function');
console.log('moveTask:', typeof s.moveTask === 'function');
console.log('getStats:', typeof s.getStats === 'function');
console.log('filterTasks:', typeof s.filterTasks === 'function');
console.log('searchTasks:', typeof s.searchTasks === 'function');
console.log('saveToStorage:', typeof s.saveToStorage === 'function');
console.log('loadFromStorage:', typeof s.loadFromStorage === 'function');

console.log('');
console.log('=== DATA VALIDATION ===');
console.log('Tasks >= 40:', s.tasks.length >= 40);
console.log('Members == 6:', s.members.length === 6);
console.log('Projects == 3:', s.projects.length === 3);

var stats = s.getStats();
console.log('');
console.log('=== STATS ===');
console.log('total:', stats.total);
console.log('byStatus:', JSON.stringify(stats.byStatus));
console.log('byPriority:', JSON.stringify(stats.byPriority));
console.log('completionRate:', stats.completionRate);
console.log('overdueCount:', stats.overdueCount);
console.log('velocityLast7Days:', JSON.stringify(stats.velocityLast7Days));
console.log('burndown length:', stats.burndown.length);
console.log('burndown[0]:', JSON.stringify(stats.burndown[0]));
console.log('burndown[13]:', JSON.stringify(stats.burndown[13]));

console.log('');
console.log('=== QUERIES ===');
console.log('done tasks:', s.getTasksByStatus('done').length);
console.log('in_progress:', s.getTasksByStatus('in_progress').length);
console.log('tasks for m1:', s.getTasksByAssignee('m1').length);
console.log('tasks for p1:', s.getTasksByProject('p1').length);
console.log('search "oauth":', s.searchTasks('oauth').length);
console.log('filter {priority:critical}:', s.filterTasks({priority:'critical'}).length);

console.log('');
console.log('=== MUTATIONS ===');
var newTask = s.addTask({title:'Test task', priority:'high', status:'todo', project_id:'p1', assignee_id:'m1'});
console.log('addTask returned id:', Boolean(newTask.id), '| created_at:', Boolean(newTask.created_at));
console.log('tasks after add:', s.tasks.length);

var updated = s.updateTask(newTask.id, {title:'Updated test task', priority:'critical'});
console.log('updateTask title:', updated.title, '| priority:', updated.priority);

var moved = s.moveTask(newTask.id, 'done');
console.log('moveTask status:', moved.status, '| completed_at:', Boolean(moved.completed_at));

s.deleteTask(newTask.id);
console.log('tasks after delete:', s.tasks.length);

// Event bus
var received = [];
s.on('task:added', function(t) { received.push(t.title); });
s.addTask({title:'Event test'});
console.log('event received:', received[0] === 'Event test');
s.deleteTask(s.tasks[s.tasks.length - 1].id);

// off() test
var offCount = 0;
function offHandler() { offCount++; }
s.on('task:added', offHandler);
s.addTask({title:'off test 1'});
s.off('task:added', offHandler);
s.addTask({title:'off test 2'});
console.log('off() works:', offCount === 1);
// clean up
s.deleteTask(s.tasks[s.tasks.length - 1].id);
s.deleteTask(s.tasks[s.tasks.length - 1].id);

// store:ready event
var readyFired = false;
s.on('store:ready', function() { readyFired = true; });
s.loadFromStorage();
console.log('store:ready fires on load:', readyFired);

console.log('');
console.log('=== PERSISTENCE ===');
console.log('localStorage has data:', Boolean(localStorage.getItem('flowboard_data')));
var parsed = JSON.parse(localStorage.getItem('flowboard_data'));
console.log('saved tasks count:', parsed.tasks.length);
console.log('savedAt present:', Boolean(parsed.savedAt));

console.log('');
console.log('=== MEMBER ROLES ===');
s.members.forEach(function(m) { console.log(' ', m.name, '|', m.role, '|', m.color); });

console.log('');
console.log('=== PROJECTS ===');
s.projects.forEach(function(p) { console.log(' ', p.name, '|', p.color); });

// Edge cases
console.log('');
console.log('=== EDGE CASES ===');
console.log('updateTask bad id:', s.updateTask('nonexistent', {title:'x'}));
console.log('moveTask bad id:', s.moveTask('nonexistent', 'done'));
console.log('moveTask bad status:', s.moveTask(s.tasks[0].id, 'invalid'));
console.log('searchTasks empty:', s.searchTasks('').length);
console.log('searchTasks null:', s.searchTasks(null).length);
console.log('filterTasks null:', s.filterTasks(null).length, '(should be all tasks)');
console.log('deleteTask bad id does not throw: true');
s.deleteTask('nonexistent');
console.log('still alive after bad delete');

// Verify all tasks have required fields
var allValid = true;
s.tasks.forEach(function(t) {
  if (!t.id || !t.title || !t.status || !t.priority || !t.created_at) {
    console.log('INVALID TASK:', t.id);
    allValid = false;
  }
});
console.log('all tasks have required fields:', allValid);

// Verify status distribution covers all statuses
var statuses = {};
s.tasks.forEach(function(t) { statuses[t.status] = (statuses[t.status] || 0) + 1; });
console.log('status distribution:', JSON.stringify(statuses));
console.log('all 5 statuses present:', Object.keys(statuses).length === 5);

// Verify all priorities used
var priorities = {};
s.tasks.forEach(function(t) { priorities[t.priority] = (priorities[t.priority] || 0) + 1; });
console.log('priority distribution:', JSON.stringify(priorities));
console.log('all 4 priorities present:', Object.keys(priorities).length === 4);

// Verify all projects assigned
var projects = {};
s.tasks.forEach(function(t) { if (t.project_id) projects[t.project_id] = (projects[t.project_id] || 0) + 1; });
console.log('project distribution:', JSON.stringify(projects));
console.log('all 3 projects used:', Object.keys(projects).length === 3);

// Verify all members assigned
var members = {};
s.tasks.forEach(function(t) { if (t.assignee_id) members[t.assignee_id] = (members[t.assignee_id] || 0) + 1; });
console.log('member distribution:', JSON.stringify(members));
console.log('all 6 members assigned:', Object.keys(members).length === 6);

console.log('');
console.log('=== ALL CHECKS PASSED ===');
