import { useMemo, useState } from 'react';
import { BarChart3, Search } from 'lucide-react';

import { Card } from '../../ui/Card.jsx';
import { EmptyState } from '../../ui/EmptyState.jsx';

const GROUP_LABELS = {
  DIMENSION: 'Dimensión',
  TOPIC: 'Tema',
  CATEGORY: 'Categoría',
  UNGROUPED: 'Sin agrupación',
};

function QuestionCard({ question }) {
  const isOrdinal = question.measurement_level === 'ORDINAL';
  const frequencies = isOrdinal
    ? [...question.frequencies].sort((a, b) => a.order - b.order)
    : [...question.frequencies].sort((a, b) => b.n - a.n || a.order - b.order);
  const maxPercentage = Math.max(1, ...frequencies.map((item) => item.percentage));

  return (
    <Card className="overflow-hidden" padded={false}>
      <div className="border-b border-border px-4 py-4 sm:px-5">
        <div className="flex flex-wrap items-start justify-between gap-3">
          <div className="min-w-0">
            <p className="font-mono text-[11px] font-semibold text-muted">{question.variable_code || question.code}</p>
            <h3 className="mt-1 text-sm font-semibold leading-5 text-dark">{question.question_text}</h3>
          </div>
          <div className="flex shrink-0 gap-2">
            <span className="rounded-lg bg-turquoiseSoft px-2 py-1 text-[10px] font-bold text-turquoiseDark">
              {question.measurement_level}
            </span>
            <span className="rounded-lg bg-amber/10 px-2 py-1 text-[10px] font-bold text-yellowDark">
              n = {question.valid_n}
            </span>
          </div>
        </div>
        {question.missing_n > 0 ? <p className="mt-2 text-[11px] text-muted">{question.missing_n} dato(s) faltante(s)</p> : null}
      </div>

      {frequencies.length ? (
        <div className="grid grid-cols-1 gap-5 p-4 sm:p-5 lg:grid-cols-2">
          <div className="space-y-3">
            {frequencies.map((item) => (
              <div key={item.code}>
                <div className="mb-1 flex items-center justify-between gap-3 text-xs">
                  <span className="truncate font-medium text-dark">{item.label}</span>
                  <span className="shrink-0 text-muted">{item.n} · {item.percentage.toFixed(1)}%</span>
                </div>
                <div className="h-2.5 overflow-hidden rounded-full bg-[#F1F3F5]">
                  <div
                    className={`h-full rounded-full ${isOrdinal ? 'bg-amber' : 'bg-turquoise'}`}
                    style={{ width: `${(item.percentage / maxPercentage) * 100}%` }}
                  />
                </div>
              </div>
            ))}
          </div>

          <div className="overflow-x-auto rounded-xl border border-border">
            <table className="w-full text-left text-xs">
              <thead className="bg-surfaceSoft text-muted">
                <tr>
                  <th className="px-3 py-2.5 font-semibold">Categoría</th>
                  <th className="px-3 py-2.5 text-right font-semibold">n</th>
                  <th className="px-3 py-2.5 text-right font-semibold">%</th>
                  {isOrdinal ? <th className="px-3 py-2.5 text-right font-semibold">% acum.</th> : null}
                </tr>
              </thead>
              <tbody>
                {frequencies.map((item) => (
                  <tr key={item.code} className="border-t border-border">
                    <td className="px-3 py-2.5 text-dark">{item.label}</td>
                    <td className="px-3 py-2.5 text-right">{item.n}</td>
                    <td className="px-3 py-2.5 text-right">{item.percentage.toFixed(1)}</td>
                    {isOrdinal ? <td className="px-3 py-2.5 text-right">{item.cumulative_percentage?.toFixed(1) ?? '—'}</td> : null}
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        </div>
      ) : question.numeric ? (
        <div className="grid grid-cols-2 gap-3 p-4 sm:grid-cols-4 sm:p-5">
          {[
            ['Media', question.numeric.mean],
            ['Mediana', question.numeric.median],
            ['Desv. estándar', question.numeric.std],
            ['Rango', question.numeric.min === null ? null : `${question.numeric.min} – ${question.numeric.max}`],
          ].map(([label, value]) => (
            <div key={label} className="rounded-xl border border-border bg-surfaceSoft/50 p-3">
              <p className="text-[10px] font-bold uppercase tracking-wide text-muted">{label}</p>
              <p className="mt-1 text-lg font-bold text-dark">{typeof value === 'number' ? value.toFixed(2) : value ?? '—'}</p>
            </div>
          ))}
        </div>
      ) : (
        <div className="p-4 text-sm text-muted">No hay valores categóricos o numéricos para resumir.</div>
      )}
    </Card>
  );
}

export default function ResponseDistributionsTab({ descriptives, isLoading }) {
  const [search, setSearch] = useState('');
  const [groupKey, setGroupKey] = useState('all');

  const questions = descriptives?.questions || [];
  const groups = descriptives?.groups || [];
  const filtered = useMemo(() => {
    const needle = search.trim().toLocaleLowerCase('es');
    return questions.filter((question) => {
      const matchesGroup = groupKey === 'all' || question.group_key === groupKey;
      const haystack = `${question.code} ${question.variable_code || ''} ${question.question_text} ${question.group_label}`.toLocaleLowerCase('es');
      return matchesGroup && (!needle || haystack.includes(needle));
    });
  }, [groupKey, questions, search]);

  if (isLoading) return <div className="h-64 animate-pulse rounded-2xl border border-border bg-white/60" />;
  if (!descriptives || questions.length === 0) {
    return (
      <Card>
        <EmptyState
          title="No hay preguntas para describir"
          description="El instrumento seleccionado todavía no contiene preguntas o no tiene una versión asociada."
        />
      </Card>
    );
  }

  const visibleGroups = groups
    .map((group) => ({ ...group, questions: filtered.filter((question) => question.group_key === group.key) }))
    .filter((group) => group.questions.length);

  return (
    <div className="space-y-5">
      <Card className="sticky top-[68px] z-[5]" padding="compact">
        <div className="flex flex-col gap-3 lg:flex-row lg:items-center">
          <label className="relative min-w-0 flex-1">
            <Search className="absolute left-3 top-1/2 h-4 w-4 -translate-y-1/2 text-muted/60" />
            <input
              className="colmena-input w-full pl-9"
              onChange={(event) => setSearch(event.target.value)}
              placeholder="Buscar pregunta, código, tema o variable…"
              type="search"
              value={search}
            />
          </label>
          <select className="colmena-input min-w-[220px]" onChange={(event) => setGroupKey(event.target.value)} value={groupKey}>
            <option value="all">Todas las agrupaciones</option>
            {groups.map((group) => (
              <option key={group.key} value={group.key}>{GROUP_LABELS[group.group_type]} · {group.label}</option>
            ))}
          </select>
          <div className="flex items-center gap-2 text-xs text-muted">
            <BarChart3 size={15} className="text-amber" />
            {filtered.length} de {questions.length} preguntas
          </div>
        </div>
      </Card>

      {visibleGroups.length ? visibleGroups.map((group) => (
        <section key={group.key} className="space-y-3">
          <div className="flex items-center gap-3">
            <div>
              <p className="text-[10px] font-bold uppercase tracking-[0.1em] text-amber">{GROUP_LABELS[group.group_type]}</p>
              <h2 className="text-sm font-bold text-dark">{group.label}</h2>
            </div>
            <div className="h-px flex-1 bg-border" />
            <span className="text-xs text-muted">{group.questions.length}</span>
          </div>
          <div className="grid grid-cols-1 gap-4 2xl:grid-cols-2">
            {group.questions.map((question) => <QuestionCard key={question.question_id} question={question} />)}
          </div>
        </section>
      )) : (
        <Card>
          <EmptyState title="Sin coincidencias" description="Cambia la búsqueda o la agrupación seleccionada." />
        </Card>
      )}
    </div>
  );
}
