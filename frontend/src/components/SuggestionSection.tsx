import { useState } from 'react';

interface SuggestionSectionProps<T> {
  title: string;
  emoji: string;
  colorClass: string; 
  items: T[];
  renderItem: (item: T, index: number) => React.ReactNode;
}

export function SuggestionSection<T>({
  title,
  emoji,
  colorClass,
  items,
  renderItem,
}: SuggestionSectionProps<T>) {
  const [isExpanded, setIsExpanded] = useState(true);

  if (!items || items.length === 0) {
    return null; 
  }

  return (
    <div className="mb-6">
      <button
        onClick={() => setIsExpanded(!isExpanded)}
        className={`w-full flex items-center justify-between px-6 py-4 ${colorClass} text-white rounded-lg border-4 border-black shadow-[6px_6px_0px_0px_rgba(0,0,0,1)] hover:shadow-[8px_8px_0px_0px_rgba(0,0,0,1)] transition-all duration-200 hover:-translate-x-[2px] hover:-translate-y-[2px]`}
      >
        <div className="flex items-center gap-3">
          <span className="text-2xl">{emoji}</span>
          <span className="font-retro text-lg font-bold">
            {title} ({items.length})
          </span>
        </div>
        <svg
          className={`w-6 h-6 transition-transform duration-200 ${
            isExpanded ? 'rotate-180' : ''
          }`}
          fill="none"
          stroke="currentColor"
          viewBox="0 0 24 24"
        >
          <path
            strokeLinecap="round"
            strokeLinejoin="round"
            strokeWidth={2}
            d="M19 9l-7 7-7-7"
          />
        </svg>
      </button>

      {isExpanded && (
        <div className="mt-4 space-y-4">
          {items.map((item, index) => (
            <div
              key={index}
              className="bg-white p-5 rounded-lg border-4 border-black shadow-[4px_4px_0px_0px_rgba(0,0,0,1)]"
            >
              {renderItem(item, index)}
            </div>
          ))}
        </div>
      )}
    </div>
  );
}
