import React from 'react';
import { EnergySiteLayout } from '../types/types';

interface SiteLayoutProps {
  energySiteLayout: EnergySiteLayout;
}

const SiteLayout: React.FC<SiteLayoutProps> = ({ energySiteLayout }) => {
  return (
    <div>
      <div className="bg-white shadow-md rounded-lg p-6 text-left">
        <h2 className="text-2xl font-bold mb-4 text-gray-800">Site Layout</h2>
        <div className="flex flex-col bg-gray-200 p-4 rounded-lg">
          {energySiteLayout.layout.map((row, rowIndex) => (
            <div key={rowIndex} className="flex mb-2">
              {row.map((item, itemIndex) => (
                <div
                  key={`${rowIndex}-${itemIndex}`}
                  className={`mr-2 flex flex-col items-center justify-center text-white text-xs font-bold ${
                    item.type === 'battery' ? 'bg-blue-500' : 'bg-green-500'
                  }`}
                  style={{
                    width: `${item.width * 5}px`,
                    height: `${item.length * 5}px`,
                  }}>
                  <span>{item.name}</span>
                </div>
              ))}
            </div>
          ))}
        </div>
      </div>
    </div>
  );
};

export default SiteLayout;
