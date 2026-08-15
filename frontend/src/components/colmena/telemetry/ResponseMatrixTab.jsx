import { useMutation } from '@tanstack/react-query';
import { Download, ShieldCheck } from 'lucide-react';

import { createExport, getExportDownloadUrl } from '../../../api/exports.js';
import { Button } from '../../ui/Button.jsx';
import { Card } from '../../ui/Card.jsx';
import { EmptyState } from '../../ui/EmptyState.jsx';

const INITIAL_ROW_LIMIT = 200;

// El backend soporta CSV, XLSX y JSON. SPSS, Power BI y Parquet están
// definidos en el esquema de exportación pero aún no implementados
// (requieren pyreadstat/polars) — se muestran deshabilitados en vez de
// ocultarse, para que el usuario sepa que existen y no se han sacado.
const AVAILABLE_EXPORT_TYPES = ['CSV', 'XLSX', 'JSON'];
const PENDING_EXPORT_TYPES = [
  { type: 'SPSS', label: 'SPSS' },
  { type: 'POWERBI', label: 'Power BI' },
  { type: 'PARQUET', label: 'Parquet' },
];

export default function ResponseMatrixTab({ studyId, dataset, descriptives, isLoading }) {
  const exportMutation = useMutation({
    mutationFn: (exportType) => createExport(studyId, {
      export_type: exportType,
      dataset_shape: 'WIDE',
    }),
    onSuccess: (result) => {
      if (result.status === 'COMPLETED') window.location.assign(getExportDownloadUrl(result.id));
    },
  });

  if (isLoading) return <div className="h-64 animate-pulse rounded-2xl border border-border bg-white/60" />;
  if (!dataset?.rows?.length) {
    return (
      <Card>
        <EmptyState
          title="Sin respuestas válidas"
          description="La matriz se construye únicamente con sesiones completas y analíticamente válidas."
        />
      </Card>
    );
  }

  const metadataByColumn = new Map();
  (descriptives?.questions || []).forEach((question) => {
    const metadata = {
      label: question.variable_label || question.short_label || question.question_text,
      group: question.group_label,
      code: question.variable_code || question.code,
    };
    metadataByColumn.set(question.code, metadata);
    if (question.variable_code) metadataByColumn.set(question.variable_code, metadata);
  });
  const columns = dataset.columns || [];
  const rows = dataset.rows.slice(0, INITIAL_ROW_LIMIT);

  return (
    <div className="space-y-4">
      <Card padding="compact">
        <div className="flex flex-col gap-3 sm:flex-row sm:items-center sm:justify-between">
          <div className="flex items-start gap-3">
            <div className="mt-0.5 rounded-xl bg-turquoiseSoft p-2 text-turquoiseDark"><ShieldCheck size={17} /></div>
            <div>
              <p className="text-sm font-semibold text-dark">Matriz anonimizada</p>
              <p className="mt-1 text-xs text-muted">
                case_id es un correlativo temporal; no se muestran tokens, correos ni sesiones incompletas.
              </p>
            </div>
          </div>
          <div className="flex flex-wrap gap-2">
            {AVAILABLE_EXPORT_TYPES.map((type) => (
              <Button
                key={type}
                loading={exportMutation.isPending && exportMutation.variables === type}
                onClick={() => exportMutation.mutate(type)}
                size="sm"
                type="button"
                variant="secondary"
              >
                <Download size={14} /> {type}
              </Button>
            ))}
            {PENDING_EXPORT_TYPES.map(({ type, label }) => (
              <span
                key={type}
                title="Formato definido en el backend, pendiente de implementación"
                className="inline-flex h-8 shrink-0 cursor-not-allowed items-center gap-1.5 rounded-lg border border-dashed border-border px-3 text-xs font-semibold text-muted opacity-70"
              >
                <Download size={14} /> {label} · pronto
              </span>
            ))}
          </div>
        </div>
        {exportMutation.isError ? <p className="mt-2 text-xs font-medium text-danger">{exportMutation.error?.message}</p> : null}
      </Card>

      <Card padded={false}>
        <div className="border-b border-border px-4 py-3 text-xs text-muted">
          Mostrando {rows.length} de {dataset.rows.length} filas · {columns.length} columnas
          {dataset.rows.length > INITIAL_ROW_LIMIT ? ' · exporta para obtener la base completa' : ''}
        </div>
        <div className="max-h-[620px] overflow-auto">
          <table className="min-w-max border-collapse text-left text-xs">
            <thead className="sticky top-0 z-[2] bg-surfaceSoft">
              <tr>
                {columns.map((column) => {
                  const metadata = metadataByColumn.get(column);
                  return (
                    <th key={column} className="min-w-[130px] border-b border-r border-border px-3 py-2.5 align-bottom last:border-r-0">
                      {metadata ? <span className="block text-[9px] font-bold uppercase tracking-wide text-amber">{metadata.group}</span> : null}
                      <span className="block max-w-[190px] truncate font-semibold text-dark" title={metadata?.label || column}>
                        {metadata?.label || column}
                      </span>
                      {metadata ? <span className="mt-0.5 block font-mono text-[9px] font-normal text-muted">{metadata.code}</span> : null}
                    </th>
                  );
                })}
              </tr>
            </thead>
            <tbody>
              {rows.map((row) => (
                <tr key={row.case_id} className="border-b border-border transition hover:bg-[#FAFBFC]">
                  {columns.map((column) => (
                    <td key={column} className="max-w-[220px] truncate border-r border-border px-3 py-2 font-mono text-dark last:border-r-0" title={String(row[column] ?? '')}>
                      {String(row[column] ?? '—')}
                    </td>
                  ))}
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      </Card>
    </div>
  );
}
