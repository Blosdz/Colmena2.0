import { lazy, Suspense } from 'react';
import { Navigate, Route, Routes } from 'react-router-dom';

import { ProtectedRoute } from './auth/AuthContext.jsx';
import { AppShell } from './components/layout/AppShell.jsx';
import { LoadingState } from './components/ui/LoadingState.jsx';

const LoginPage = lazy(() => import('./pages/DemoAccessPage.jsx'));
const SignupPage = lazy(() => import('./pages/SignupPage.jsx'));
const PublicSurveyPage = lazy(() => import('./pages/PublicSurveyPage.jsx'));
const DashboardPage = lazy(() => import('./pages/colmena/CompanyDashboardPage.jsx'));
const CompanyProfilePage = lazy(() => import('./pages/colmena/CompanyProfilePage.jsx'));
const CampaignWizardPage = lazy(() => import('./pages/colmena/CampaignWizardPage.jsx'));
const CampaignOverviewPage = lazy(() => import('./pages/colmena/project/CampaignOverviewPage.jsx'));
const DemoCampaignPage = lazy(() => import('./pages/colmena/DemoCampaignPage.jsx'));
const ArchiveProjectsPage = lazy(() => import('./pages/colmena/ArchiveProjectsPage.jsx'));
const SettingsPage = lazy(() => import('./pages/colmena/SettingsPage.jsx'));
const NotFoundPage = lazy(() => import('./pages/colmena/NotFoundPage.jsx'));
const ProjectConstructorPage = lazy(() => import('./pages/colmena/project/ProjectConstructorPage.jsx'));
const ProjectFormPage = lazy(() => import('./pages/colmena/project/ProjectFormPage.jsx'));
const ProjectLinkPage = lazy(() => import('./pages/colmena/project/ProjectLinkPage.jsx'));
const ProjectTelemetryPage = lazy(() => import('./pages/colmena/project/AdaptiveProjectTelemetryPage.jsx'));
const ProjectAnalysisPage = lazy(() => import('./pages/colmena/project/ProjectAnalyticsLabPage.jsx'));
const ProjectReportsPage = lazy(() => import('./pages/colmena/project/CompanyReportPage.jsx'));
const ProjectPremiumDashboardPage = lazy(() => import('./pages/colmena/project/ProjectPremiumDashboardPage.jsx'));

export default function App() {
  return (
    <Suspense fallback={<LoadingState label="Cargando página…" />}>
      <Routes>
      <Route path="/login" element={<LoginPage />} />
      <Route path="/signup" element={<SignupPage />} />
      <Route path="/encuesta/:publicId" element={<PublicSurveyPage />} />

      <Route
        path="/colmena"
        element={
          <ProtectedRoute>
            <AppShell />
          </ProtectedRoute>
        }
      >
        <Route index element={<DashboardPage />} />
        <Route path="company" element={<CompanyProfilePage />} />
        <Route path="campaign/new" element={<CampaignWizardPage />} />
        <Route path="demo" element={<DemoCampaignPage />} />

        <Route path="project/new" element={<ProjectConstructorPage />} />
        <Route path="project/:projectId" element={<CampaignOverviewPage />} />
        <Route path="project/:projectId/admin" element={<ProjectConstructorPage />} />
        <Route path="project/:projectId/form" element={<ProjectFormPage />} />
        <Route path="project/:projectId/link" element={<ProjectLinkPage />} />
        <Route path="project/:projectId/telemetry" element={<ProjectTelemetryPage />} />
        <Route path="project/:projectId/results" element={<ProjectPremiumDashboardPage />} />
        <Route path="project/:projectId/analysis" element={<ProjectAnalysisPage />} />
        <Route path="project/:projectId/premium" element={<ProjectPremiumDashboardPage />} />
        <Route path="project/:projectId/reports" element={<ProjectReportsPage />} />

        <Route path="archive/projects" element={<ArchiveProjectsPage />} />
        <Route path="settings" element={<SettingsPage />} />

        <Route path="*" element={<NotFoundPage />} />
      </Route>

      <Route path="/" element={<Navigate to="/colmena" replace />} />
      <Route path="*" element={<Navigate to="/colmena" replace />} />
      </Routes>
    </Suspense>
  );
}
