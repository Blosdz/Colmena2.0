import {
  Area,
  AreaChart,
  CartesianGrid,
  ResponsiveContainer,
  Tooltip,
  XAxis,
  YAxis,
} from 'recharts';
import { Activity, CheckCircle2, Clock, FileCheck2, Users } from 'lucide-react';

import { Card } from '../../ui/Card.jsx';
import MetricCard from '../../ui/MetricCard.jsx';
import { EmptyState } from '../../ui/EmptyState.jsx';

function formatDuration(seconds) {
  if (seconds === null || seconds === undefined) return '—';
  const rounded = Math.round(seconds);
  if (rounded < 60) return `${rounded}s`;
  return `${Math.floor(rounded / 60)}m ${rounded % 60}s`;
}

export default function TelemetrySummaryTab({ telemetry, overview, isLoading }) {
  if (isLoading) {
    return <div className="h-48 animate-pulse rounded-2xl border border-border bg-white/60" />;
  }
  if (!telemetry) {
    return (
      <Card>
        <EmptyState
          title="Todavía no hay telemetría"
          description="Elige una aplicación con sesiones para ver participación y calidad de respuesta."
        />
      </Card>
    );
  }

  const roots = (overview?.results || []).filter((result) => result.parent_id === null);
  const completionRate = telemetry.started_count
    ? Math.round((telemetry.completed_count / telemetry.started_count) * 100)
    : null;

  return (
    <div className="space-y-4">
      <div className="grid grid-cols-1 gap-4 sm:grid-cols-2 xl:grid-cols-5">
        <MetricCard icon={Users} label="Sesiones iniciadas" value={telemetry.started_count} />
        <MetricCard icon={FileCheck2} label="Completadas" value={telemetry.completed_count} />
        <MetricCard icon={CheckCircle2} label="Respuestas válidas" value={telemetry.valid_count} />
        <MetricCard icon={Activity} label="Finalización" value={completionRate === null ? '—' : `${completionRate}%`} />
        <MetricCard icon={Clock} label="Duración promedio" value={formatDuration(telemetry.avg_duration_seconds)} />
      </div>

      <div className="grid grid-cols-1 gap-4 xl:grid-cols-[minmax(0,2fr)_minmax(260px,1fr)]">
        <Card>
          <p className="text-sm font-semibold text-dark">Evolución temporal</p>
          <p className="mb-4 mt-1 text-xs text-muted">Sesiones iniciadas y completadas por día.</p>
          {telemetry.series?.length ? (
            <div className="h-64 w-full">
              <ResponsiveContainer width="100%" height="100%">
                <AreaChart data={telemetry.series}>
                  <defs>
                    <linearGradient id="telemetryStarted" x1="0" x2="0" y1="0" y2="1">
                      <stop offset="0%" stopColor="#F5B21A" stopOpacity={0.32} />
                      <stop offset="100%" stopColor="#F5B21A" stopOpacity={0.02} />
                    </linearGradient>
                  </defs>
                  <CartesianGrid stroke="rgba(148,163,184,0.22)" strokeDasharray="3 3" />
                  <XAxis dataKey="date" tick={{ fontSize: 11 }} />
                  <YAxis allowDecimals={false} tick={{ fontSize: 11 }} />
                  <Tooltip />
                  <Area dataKey="started" name="Iniciadas" stroke="#F5B21A" fill="url(#telemetryStarted)" strokeWidth={2} />
                  <Area dataKey="completed" name="Completadas" stroke="#11B7B2" fill="transparent" strokeWidth={2} />
                </AreaChart>
              </ResponsiveContainer>
            </div>
          ) : (
            <EmptyState title="Sin evolución todavía" description="La serie aparecerá con las primeras sesiones." />
          )}
        </Card>

        <Card>
          <p className="text-sm font-semibold text-dark">Calidad de los casos</p>
          <p className="mt-1 text-xs text-muted">Los análisis y la matriz usan únicamente casos válidos.</p>
          <dl className="mt-5 space-y-3 text-sm">
            {[
              ['Válidas', telemetry.valid_count, 'text-success'],
              ['En revisión', telemetry.review_count, 'text-warning'],
              ['Excluidas', telemetry.excluded_count, 'text-danger'],
              ['Abandonadas', telemetry.abandoned_count, 'text-muted'],
            ].map(([label, value, tone]) => (
              <div key={label} className="flex items-center justify-between border-b border-border/70 pb-3 last:border-0">
                <dt className="text-muted">{label}</dt>
                <dd className={`font-bold ${tone}`}>{value}</dd>
              </div>
            ))}
          </dl>
        </Card>
      </div>

      <Card>
        <p className="text-sm font-semibold text-dark">Puntajes de constructos existentes</p>
        <p className="mb-4 mt-1 text-xs text-muted">
          Se muestran sólo puntajes ya calculados; los temas visuales no generan scoring.
        </p>
        {roots.length ? (
          <div className="grid grid-cols-1 gap-3 sm:grid-cols-2 xl:grid-cols-4">
            {roots.map((root) => (
              <div key={root.construct_id} className="rounded-2xl border border-border bg-surfaceSoft/60 p-4">
                <p className="truncate text-xs font-semibold text-muted">{root.construct_name}</p>
                <p className="mt-2 text-2xl font-bold text-dark">
                  {root.suppressed || root.mean_score === null ? 'Suprimido' : `${Number(root.mean_score).toFixed(1)} / 100`}
                </p>
                <p className="mt-1 text-[11px] text-muted">n = {root.n_valid ?? 0}</p>
              </div>
            ))}
          </div>
        ) : (
          <div className="rounded-2xl border border-dashed border-border bg-surfaceSoft/40 p-5 text-sm text-muted">
            Este instrumento no tiene puntajes calculados. Sus preguntas siguen disponibles en Distribuciones.
          </div>
        )}
      </Card>
    </div>
  );
}
