import { Clock, Filter } from "lucide-react";
import { useTranslation } from "react-i18next";

const TIME_RANGES = [
  { labelKey: "filter.10m", hours: 0.167 },
  { labelKey: "filter.1h", hours: 1 },
  { labelKey: "filter.24h", hours: 24 },
  { labelKey: "filter.7d", hours: 168 },
];

const CATEGORY_FILTERS = [
  { labelKey: "filter.all", value: "all" },
  { labelKey: "category.blocked", value: "blocked" },
  { labelKey: "category.spam", value: "spam" },
  { labelKey: "category.nsfw", value: "nsfw" },
  { labelKey: "filter.highSeverity", value: "high" },
];

export default function DashboardFilters({ timeRange, setTimeRange, categoryFilter, setCategoryFilter }) {
  const { t } = useTranslation();

  return (
    <div className="flex flex-wrap items-center gap-3">
      {/* Time range */}
      <div className="flex items-center gap-1.5 bg-white/80 rounded-xl border border-gray-200/60 p-1 shadow-sm">
        <Clock className="w-3.5 h-3.5 text-gray-400 ml-2" />
        {TIME_RANGES.map((tr) => (
          <button
            key={tr.hours}
            onClick={() => setTimeRange(tr.hours)}
            className={`px-3 py-1.5 rounded-lg text-xs font-medium transition-all ${
              timeRange === tr.hours
                ? "bg-gray-900 text-white shadow-sm"
                : "text-gray-500 hover:text-gray-800 hover:bg-gray-100"
            }`}
          >
            {t(tr.labelKey)}
          </button>
        ))}
      </div>

      {/* Category filters */}
      <div className="flex items-center gap-1.5 bg-white/80 rounded-xl border border-gray-200/60 p-1 shadow-sm">
        <Filter className="w-3.5 h-3.5 text-gray-400 ml-2" />
        {CATEGORY_FILTERS.map((c) => (
          <button
            key={c.value}
            onClick={() => setCategoryFilter(c.value)}
            className={`px-3 py-1.5 rounded-lg text-xs font-medium transition-all ${
              categoryFilter === c.value
                ? "bg-gray-900 text-white shadow-sm"
                : "text-gray-500 hover:text-gray-800 hover:bg-gray-100"
            }`}
          >
            {t(c.labelKey)}
          </button>
        ))}
      </div>
    </div>
  );
}

