import React from 'react';
import { Tooltip } from 'react-tooltip';
import { Battery, EnergySiteLayout, Transformer } from '../types/types';

interface SiteLayoutProps {
  energySiteLayout: EnergySiteLayout;
  batteries: Battery[];
  transformer: Transformer;
}

const SiteLayout: React.FC<SiteLayoutProps> = ({ energySiteLayout, batteries, transformer }) => {
  const getItemLabel = (item: { type: string; id: number }) => {
    if (item.type === 'battery') {
      return `B${item.id}`;
    } else if (item.type === 'transformer') {
      return `T${item.id}`;
    }
    return '';
  };

  const getItemColor = (item: { type: string; id: number }) => {
    if (item.type === 'battery') {
      const battery = batteries.find((b) => b.id === item.id);
      return battery?.color || '#3B82F6'; // Default blue color
    } else if (item.type === 'transformer') {
      return transformer.color || '#10B981'; // Default green color
    }
    return '#6B7280'; // Default gray color
  };

  const getItemTooltipContent = (item: { type: string; id: number }) => {
    if (item.type === 'battery') {
      const battery = batteries.find((b) => b.id === item.id);
      if (battery) {
        return (
          <div className="text-sm">
            <h3 className="font-bold text-lg mb-2">{battery.name}</h3>
            <p>
              <span className="font-semibold">Dimensions: </span>
              {battery.dimensions.width}x{battery.dimensions.length}
              {battery.dimensions.unit}
            </p>
            <p>
              <span className="font-semibold">Energy:</span> {battery.energy} {battery.energyUnit}
            </p>
            <p>
              <span className="font-semibold">Cost:</span> {battery.cost} {battery.costCurrency}
            </p>
            <p>
              <span className="font-semibold">Release Date:</span> {battery.releaseDate}
            </p>
          </div>
        );
      }
      return <p>Battery data not found</p>;
    } else if (item.type === 'transformer') {
      return (
        <div className="text-sm">
          <h3 className="font-bold text-lg mb-2">{transformer.name}</h3>
          <p>
            <span className="font-semibold">Dimensions:</span> {transformer.dimensions.length}x
            {transformer.dimensions.width} {transformer.dimensions.unit}
          </p>
          <p>
            <span className="font-semibold">Energy:</span> {transformer.energy}{' '}
            {transformer.energyUnit}
          </p>
          <p>
            <span className="font-semibold">Cost:</span> {transformer.cost}{' '}
            {transformer.costCurrency}
          </p>
          <p>
            <span className="font-semibold">Release Date:</span> {transformer.releaseDate}
          </p>
        </div>
      );
    }
    return null;
  };

  return (
    <div>
      <div className="bg-white shadow-md rounded-lg p-6 text-left">
        <h2 className="text-2xl font-bold mb-4 text-gray-800">Site Layout</h2>
        <div className="flex flex-col p-4 rounded-lg">
          {energySiteLayout.layout.map((row, rowIndex) => (
            <div key={rowIndex} className="flex mb-2">
              {row.map((item, itemIndex) => (
                <React.Fragment key={`${rowIndex}-${itemIndex}`}>
                  <div
                    data-tooltip-id={`tooltip-${item.type}-${item.id}`}
                    className={`mr-2 flex flex-col items-center justify-center text-white text-xs font-bold cursor-pointer`}
                    style={{
                      width: `${item.width * 5}px`,
                      height: `${item.length * 5}px`,
                      backgroundColor: getItemColor(item),
                    }}>
                    <span>{getItemLabel(item)}</span>
                  </div>
                  <Tooltip
                    id={`tooltip-${item.type}-${item.id}`}
                    place="top"
                    className="max-w-xs"
                    style={{
                      backgroundColor: getItemColor(item),
                      color: '#FFFFFF',
                    }}>
                    {getItemTooltipContent(item)}
                  </Tooltip>
                </React.Fragment>
              ))}
            </div>
          ))}
        </div>
      </div>
    </div>
  );
};

export default SiteLayout;
