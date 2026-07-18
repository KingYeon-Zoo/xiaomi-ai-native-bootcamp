import ModelMetricsDashboard from "../components/ModelMetrics/ModelMetricsDashboard";

export default function MetricsDashboardPage({ setActiveTab }) {
  return (
    <div className="w-full max-w-[1600px] mx-auto">
      <ModelMetricsDashboard setActiveTab={setActiveTab} />
    </div>
  );
}
