import { useState } from 'react';
import { Link } from 'react-router-dom';
import { useQuery } from '@tanstack/react-query';
import { LayoutDashboard } from 'lucide-react';

import { getResultsOverview } from '../../../api/studies.js';
import { listExogenousFields } from '../../../api/variables.js';
import { Card } from '../../ui/Card.jsx';
import { EmptyState } from '../../ui/EmptyState.jsx';
import { LoadingState } from '../../ui/LoadingState.jsx';
import MetricCard from '../../ui/MetricCard.jsx';
import StudySelector from '../StudySelector.jsx';
import DimensionChartCard from './DimensionChartCard.jsx';

export default function DimensionDashboardTab({ projectId }) {
  const [studyId, setStudyId] = useState(null);

  const { data: overview, isLoading } = useQuery({
    queryKey: ['resultsOverview', studyId],
    queryFn: () => getResultsOverview(studyId),
    enabled: Boolean(studyId),
  });
  const { data: exogenousFields = [] } = useQuery({
    queryKey: ['exogenousFields', projectId],
    queryFn: () => listExogenousFields(projectId),
    enabled: Boolean(projectId),
  });

  const results = overview?.results || [];
  const roots = results.filter((result) => result.parent_id === null);
  const dimensions = results.filter((result) => result.construct_type === 'DIMENSION');
  const childrenByParent = new Map();
  results.forEach((result) => {
    const siblings = childrenByParent.get(result.parent_id) || [];
    siblings.push(result);
    childrenByParent.set(result.parent_id, siblings);
  });

  return (
    <div className="flex flex-col gap-4 p-4">
      <Card>
        <StudySelector projectId={projectId} studyId={studyId} onStudyChange={setStudyId} />
      </Card>

      {!studyId ? (
        <EmptyState title="Elige una aplicación o estudio." description="Los puntajes por dimensión se calculan por cada aplicación del instrumento." />
      ) : isLoading ? (
        <LoadingState label="Cargando resultados…" />
      ) : results.length === 0 ? (
        <EmptyState
          title="Aún no hay resultados calculados"
          description="Ve a Resultados → Baremos y ejecuta el cálculo antes de armar el dashboard."
        >
          <Link to={`/colmena/project/${projectId}/results`} className="colmena-badge inline-flex bg-amber/10 text-yellowDark">
            Ir a Resultados
          </Link>
        </EmptyState>
      ) : dimensions.length === 0 ? (
        <EmptyState title="Sin dimensiones" description="Este instrumento no tiene constructos de tipo dimensión configurados." />
      ) : (
        <>
          {roots.length ? (
            <div className="grid grid-cols-1 gap-4 sm:grid-cols-3">
              {roots.map((root) => (
                <MetricCard
                  key={root.construct_id}
                  icon={LayoutDashboard}
                  label={root.construct_name}
                  value={root.suppressed ? 'Suprimido' : `${Math.round(root.mean_score ?? 0)} / 100`}
                />
              ))}
            </div>
          ) : null}

          <div className="grid grid-cols-1 gap-4 xl:grid-cols-2">
            {dimensions.map((dimension) => (
              <DimensionChartCard
                key={dimension.construct_id}
                studyId={studyId}
                versionId={overview?.instrument_version_id}
                dimension={dimension}
                subdimensions={childrenByParent.get(dimension.construct_id) || []}
                exogenousFields={exogenousFields}
              />
            ))}
          </div>
        </>
      )}
    </div>
  );
}
