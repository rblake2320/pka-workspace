// FlowBoard Analytics — Canvas 2D charts, zero external dependencies
(function () {
  'use strict';

  // ── Shared palette ────────────────────────────────────────────────────────
  var BG_COLOR       = '#1A1B2E';
  var LABEL_COLOR    = '#94A3B8';
  var GRID_COLOR     = 'rgba(148,163,184,0.12)';
  var AXIS_COLOR     = 'rgba(148,163,184,0.25)';

  var STATUS_COLORS = {
    backlog:     '#64748B',
    todo:        '#7C6BF2',
    in_progress: '#F59E0B',
    review:      '#06B6D4',
    done:        '#22C55E'
  };

  var STATUS_LABELS = {
    backlog:     'Backlog',
    todo:        'To Do',
    in_progress: 'In Progress',
    review:      'Review',
    done:        'Done'
  };

  var PRIORITY_COLORS = {
    critical: '#EF4444',
    high:     '#F59E0B',
    medium:   '#7C6BF2',
    low:      '#64748B'
  };

  var PRIORITY_LABELS = {
    critical: 'Critical',
    high:     'High',
    medium:   'Medium',
    low:      'Low'
  };

  // ── Helper: get canvas + context ─────────────────────────────────────────
  function getCtx(id) {
    var canvas = document.getElementById(id);
    if (!canvas) return null;
    var ctx = canvas.getContext('2d');
    // Clear for re-renders
    ctx.clearRect(0, 0, canvas.width, canvas.height);
    return { ctx: ctx, w: canvas.width, h: canvas.height };
  }

  // ── Helper: fill canvas background ───────────────────────────────────────
  function fillBg(ctx, w, h) {
    ctx.fillStyle = BG_COLOR;
    ctx.fillRect(0, 0, w, h);
  }

  // ── Helper: draw text ────────────────────────────────────────────────────
  function text(ctx, str, x, y, opts) {
    opts = opts || {};
    ctx.save();
    ctx.fillStyle    = opts.color    || LABEL_COLOR;
    ctx.font         = (opts.bold ? 'bold ' : '') + (opts.size || 11) + 'px system-ui,sans-serif';
    ctx.textAlign    = opts.align    || 'left';
    ctx.textBaseline = opts.baseline || 'alphabetic';
    ctx.fillText(String(str), x, y);
    ctx.restore();
  }

  // ── Helper: format short date label ─────────────────────────────────────
  function shortDate(dateStr) {
    if (!dateStr) return '';
    var parts = dateStr.split('-');
    if (parts.length !== 3) return dateStr;
    var d = new Date(parseInt(parts[0], 10), parseInt(parts[1], 10) - 1, parseInt(parts[2], 10));
    return d.toLocaleDateString(undefined, { month: 'short', day: 'numeric' });
  }

  // ── Helper: day-of-week label for velocity ───────────────────────────────
  function dayLabel(daysAgoIndex, totalDays) {
    // daysAgoIndex: 0 = oldest day, totalDays-1 = today
    var d = new Date();
    d.setDate(d.getDate() - (totalDays - 1 - daysAgoIndex));
    return d.toLocaleDateString(undefined, { weekday: 'short' });
  }

  // ── Chart 1: Velocity bar chart ──────────────────────────────────────────
  //  Canvas: 400 x 200 (#velocity-chart)
  //  Data:   stats.velocityLast7Days — array of 7 numbers

  function drawVelocityChart(stats) {
    var c = getCtx('velocity-chart');
    if (!c) return;
    var ctx = c.ctx, w = c.w, h = c.h;

    fillBg(ctx, w, h);

    var data  = stats.velocityLast7Days;   // [7]
    var n     = data.length;               // 7
    var maxVal = 0;
    for (var i = 0; i < n; i++) { if (data[i] > maxVal) maxVal = data[i]; }
    if (maxVal === 0) maxVal = 1; // avoid divide-by-zero

    // Layout
    var padLeft   = 36;
    var padRight  = 16;
    var padTop    = 20;
    var padBottom = 36;
    var chartW    = w - padLeft - padRight;
    var chartH    = h - padTop - padBottom;

    // Grid lines (4 horizontal)
    var gridLines = 4;
    for (var g = 0; g <= gridLines; g++) {
      var gy = padTop + chartH - (g / gridLines) * chartH;
      ctx.save();
      ctx.strokeStyle = GRID_COLOR;
      ctx.lineWidth   = 1;
      ctx.beginPath();
      ctx.moveTo(padLeft, gy);
      ctx.lineTo(padLeft + chartW, gy);
      ctx.stroke();
      ctx.restore();

      var gridVal = Math.round((g / gridLines) * maxVal);
      text(ctx, gridVal, padLeft - 6, gy + 4, { align: 'right', size: 10 });
    }

    // Y-axis line
    ctx.save();
    ctx.strokeStyle = AXIS_COLOR;
    ctx.lineWidth   = 1;
    ctx.beginPath();
    ctx.moveTo(padLeft, padTop);
    ctx.lineTo(padLeft, padTop + chartH);
    ctx.stroke();
    ctx.restore();

    // X-axis line
    ctx.save();
    ctx.strokeStyle = AXIS_COLOR;
    ctx.lineWidth   = 1;
    ctx.beginPath();
    ctx.moveTo(padLeft, padTop + chartH);
    ctx.lineTo(padLeft + chartW, padTop + chartH);
    ctx.stroke();
    ctx.restore();

    // Bars
    var barGap    = chartW * 0.12 / n;
    var barWidth  = (chartW - barGap * (n + 1)) / n;

    for (var b = 0; b < n; b++) {
      var val    = data[b];
      var barH   = (val / maxVal) * chartH;
      var bx     = padLeft + barGap + b * (barWidth + barGap);
      var by     = padTop + chartH - barH;

      // Bar with rounded top
      ctx.save();
      ctx.fillStyle = '#7C6BF2';
      var radius = Math.min(4, barWidth / 2);
      if (barH > 0) {
        ctx.beginPath();
        ctx.moveTo(bx + radius, by);
        ctx.lineTo(bx + barWidth - radius, by);
        ctx.quadraticCurveTo(bx + barWidth, by, bx + barWidth, by + radius);
        ctx.lineTo(bx + barWidth, by + barH);
        ctx.lineTo(bx, by + barH);
        ctx.lineTo(bx, by + radius);
        ctx.quadraticCurveTo(bx, by, bx + radius, by);
        ctx.closePath();
        ctx.fill();
      }
      ctx.restore();

      // Value label on top of bar
      if (val > 0) {
        text(ctx, val, bx + barWidth / 2, by - 4, { align: 'center', size: 10, color: '#CBD5E1' });
      }

      // X-axis label
      text(ctx, dayLabel(b, n), bx + barWidth / 2, padTop + chartH + 16, { align: 'center', size: 10 });
    }

    // Chart title
    text(ctx, 'Velocity — Tasks Completed (last 7 days)', padLeft, 13, { size: 11, color: '#CBD5E1', bold: true });
  }

  // ── Chart 2: Burndown line chart ─────────────────────────────────────────
  //  Canvas: 400 x 200 (#burndown-chart)
  //  Data:   stats.burndown — [{date, remaining}] x14

  function drawBurndownChart(stats) {
    var c = getCtx('burndown-chart');
    if (!c) return;
    var ctx = c.ctx, w = c.w, h = c.h;

    fillBg(ctx, w, h);

    var data = stats.burndown;  // [{date, remaining}]
    var n    = data.length;
    if (n === 0) return;

    var maxVal = 0;
    for (var i = 0; i < n; i++) { if (data[i].remaining > maxVal) maxVal = data[i].remaining; }
    if (maxVal === 0) maxVal = 1;

    // Layout
    var padLeft   = 40;
    var padRight  = 16;
    var padTop    = 20;
    var padBottom = 36;
    var chartW    = w - padLeft - padRight;
    var chartH    = h - padTop - padBottom;

    // Grid lines
    var gridLines = 4;
    for (var g = 0; g <= gridLines; g++) {
      var gy = padTop + chartH - (g / gridLines) * chartH;
      ctx.save();
      ctx.strokeStyle = GRID_COLOR;
      ctx.lineWidth   = 1;
      ctx.beginPath();
      ctx.moveTo(padLeft, gy);
      ctx.lineTo(padLeft + chartW, gy);
      ctx.stroke();
      ctx.restore();

      var gridVal = Math.round((g / gridLines) * maxVal);
      text(ctx, gridVal, padLeft - 6, gy + 4, { align: 'right', size: 10 });
    }

    // Axes
    ctx.save();
    ctx.strokeStyle = AXIS_COLOR;
    ctx.lineWidth   = 1;
    ctx.beginPath();
    ctx.moveTo(padLeft, padTop);
    ctx.lineTo(padLeft, padTop + chartH);
    ctx.lineTo(padLeft + chartW, padTop + chartH);
    ctx.stroke();
    ctx.restore();

    // Point coordinates
    var pts = [];
    for (var p = 0; p < n; p++) {
      var px = padLeft + (p / (n - 1)) * chartW;
      var py = padTop  + chartH - (data[p].remaining / maxVal) * chartH;
      pts.push({ x: px, y: py });
    }

    // Filled area
    ctx.save();
    ctx.beginPath();
    ctx.moveTo(pts[0].x, padTop + chartH);
    ctx.lineTo(pts[0].x, pts[0].y);
    for (var l = 1; l < pts.length; l++) {
      ctx.lineTo(pts[l].x, pts[l].y);
    }
    ctx.lineTo(pts[pts.length - 1].x, padTop + chartH);
    ctx.closePath();
    ctx.fillStyle = 'rgba(34,197,94,0.10)';
    ctx.fill();
    ctx.restore();

    // Line
    ctx.save();
    ctx.strokeStyle = '#22C55E';
    ctx.lineWidth   = 2;
    ctx.lineJoin    = 'round';
    ctx.beginPath();
    ctx.moveTo(pts[0].x, pts[0].y);
    for (var ll = 1; ll < pts.length; ll++) {
      ctx.lineTo(pts[ll].x, pts[ll].y);
    }
    ctx.stroke();
    ctx.restore();

    // Data points
    for (var d = 0; d < pts.length; d++) {
      ctx.save();
      ctx.fillStyle   = '#22C55E';
      ctx.strokeStyle = BG_COLOR;
      ctx.lineWidth   = 2;
      ctx.beginPath();
      ctx.arc(pts[d].x, pts[d].y, 3.5, 0, Math.PI * 2);
      ctx.fill();
      ctx.stroke();
      ctx.restore();
    }

    // X-axis labels — show every other one to avoid crowding
    for (var xl = 0; xl < n; xl++) {
      if (xl % 2 !== 0) continue;
      text(ctx, shortDate(data[xl].date), pts[xl].x, padTop + chartH + 16,
        { align: 'center', size: 9 });
    }

    // Chart title
    text(ctx, 'Burndown — Remaining Tasks (last 14 days)', padLeft, 13,
      { size: 11, color: '#CBD5E1', bold: true });
  }

  // ── Donut chart helper ────────────────────────────────────────────────────
  //  slices: [{label, value, color}]
  //  cx, cy: center; outerR, innerR: radii

  function drawDonut(ctx, cx, cy, outerR, innerR, slices, totalLabel) {
    var total = 0;
    for (var i = 0; i < slices.length; i++) { total += slices[i].value; }
    if (total === 0) {
      // Draw empty ring
      ctx.save();
      ctx.strokeStyle = 'rgba(148,163,184,0.15)';
      ctx.lineWidth   = outerR - innerR;
      ctx.beginPath();
      ctx.arc(cx, cy, (outerR + innerR) / 2, 0, Math.PI * 2);
      ctx.stroke();
      ctx.restore();
      text(ctx, '0', cx, cy + 5, { align: 'center', size: 18, bold: true, color: '#CBD5E1' });
      return;
    }

    var startAngle = -Math.PI / 2;  // start at 12 o'clock
    var gap        = slices.length > 1 ? 0.025 : 0;  // small gap between slices

    for (var s = 0; s < slices.length; s++) {
      if (slices[s].value === 0) continue;
      var sweepAngle = (slices[s].value / total) * Math.PI * 2 - gap;
      if (sweepAngle < 0) sweepAngle = 0;

      ctx.save();
      ctx.beginPath();
      ctx.arc(cx, cy, outerR, startAngle + gap / 2, startAngle + gap / 2 + sweepAngle);
      ctx.arc(cx, cy, innerR, startAngle + gap / 2 + sweepAngle, startAngle + gap / 2, true);
      ctx.closePath();
      ctx.fillStyle = slices[s].color;
      ctx.fill();
      ctx.restore();

      startAngle += sweepAngle + gap;
    }

    // Centre total label
    if (totalLabel != null) {
      text(ctx, totalLabel, cx, cy + 5,  { align: 'center', size: 18, bold: true, color: '#F1F5F9' });
      text(ctx, 'total',    cx, cy + 19, { align: 'center', size: 10, color: LABEL_COLOR });
    }
  }

  // ── Legend helper ─────────────────────────────────────────────────────────
  function drawLegend(ctx, startX, startY, slices, itemW) {
    var cols     = 2;
    var rowH     = 20;
    var dotSize  = 8;

    for (var i = 0; i < slices.length; i++) {
      var col  = i % cols;
      var row  = Math.floor(i / cols);
      var lx   = startX + col * itemW;
      var ly   = startY + row * rowH;

      // Color dot
      ctx.save();
      ctx.fillStyle = slices[i].color;
      ctx.beginPath();
      ctx.arc(lx + dotSize / 2, ly, dotSize / 2, 0, Math.PI * 2);
      ctx.fill();
      ctx.restore();

      // Label + count
      text(ctx, slices[i].label + ' · ' + slices[i].value,
        lx + dotSize + 5, ly + 4,
        { size: 10, color: LABEL_COLOR });
    }
  }

  // ── Chart 3: Status donut (#distribution-chart) ──────────────────────────
  //  Canvas: 300 x 300

  function drawStatusDonut(stats) {
    var c = getCtx('distribution-chart');
    if (!c) return;
    var ctx = c.ctx, w = c.w, h = c.h;

    fillBg(ctx, w, h);

    var byStatus = stats.byStatus;
    var statusKeys = ['backlog', 'todo', 'in_progress', 'review', 'done'];

    var slices = [];
    var total  = 0;
    for (var i = 0; i < statusKeys.length; i++) {
      var key = statusKeys[i];
      var val = byStatus[key] || 0;
      total  += val;
      slices.push({
        label: STATUS_LABELS[key],
        value: val,
        color: STATUS_COLORS[key]
      });
    }

    // Chart title
    text(ctx, 'Status Distribution', 12, 18, { size: 11, color: '#CBD5E1', bold: true });

    var donutTop    = 30;
    var legendGap   = 10;
    var legendH     = Math.ceil(slices.length / 2) * 20;
    var donutAreaH  = h - donutTop - legendGap - legendH - 10;
    var cx          = w / 2;
    var cy          = donutTop + donutAreaH / 2;
    var outerR      = Math.min(donutAreaH, w) * 0.42;
    var innerR      = outerR * 0.60;

    drawDonut(ctx, cx, cy, outerR, innerR, slices, total);

    var legendX = 10;
    var legendY = donutTop + donutAreaH + legendGap + 10;
    drawLegend(ctx, legendX, legendY, slices, (w - legendX * 2) / 2);
  }

  // ── Chart 4: Priority donut (#priority-chart) ────────────────────────────
  //  Canvas: 300 x 300

  function drawPriorityDonut(stats) {
    var c = getCtx('priority-chart');
    if (!c) return;
    var ctx = c.ctx, w = c.w, h = c.h;

    fillBg(ctx, w, h);

    var byPriority    = stats.byPriority;
    var priorityKeys  = ['critical', 'high', 'medium', 'low'];

    var slices = [];
    var total  = 0;
    for (var i = 0; i < priorityKeys.length; i++) {
      var key = priorityKeys[i];
      var val = byPriority[key] || 0;
      total  += val;
      slices.push({
        label: PRIORITY_LABELS[key],
        value: val,
        color: PRIORITY_COLORS[key]
      });
    }

    // Chart title
    text(ctx, 'Priority Breakdown', 12, 18, { size: 11, color: '#CBD5E1', bold: true });

    var donutTop   = 30;
    var legendGap  = 10;
    var legendH    = Math.ceil(slices.length / 2) * 20;
    var donutAreaH = h - donutTop - legendGap - legendH - 10;
    var cx         = w / 2;
    var cy         = donutTop + donutAreaH / 2;
    var outerR     = Math.min(donutAreaH, w) * 0.42;
    var innerR     = outerR * 0.60;

    drawDonut(ctx, cx, cy, outerR, innerR, slices, total);

    var legendX = 10;
    var legendY = donutTop + donutAreaH + legendGap + 10;
    drawLegend(ctx, legendX, legendY, slices, (w - legendX * 2) / 2);
  }

  // ── Main entry point ──────────────────────────────────────────────────────
  function renderAnalytics() {
    var stats = window.store.getStats();
    drawVelocityChart(stats);
    drawBurndownChart(stats);
    drawStatusDonut(stats);
    drawPriorityDonut(stats);
  }

  // ── Expose globally ───────────────────────────────────────────────────────
  window.analytics = {
    renderAnalytics: renderAnalytics
  };

})();
