import React from 'react';

const energySiteLayout = {
  maxWidth: 100,
  dimensions: {
    length: 40,
    width: 100,
    unit: 'ft',
  },
  layout: [
    [
      {
        type: 'battery',
        id: 4,
        name: 'Powerpack',
        width: 10,
        length: 10,
      },
      {
        type: 'battery',
        id: 2,
        name: 'Megapack 2',
        width: 30,
        length: 10,
      },
      {
        type: 'battery',
        id: 1,
        name: 'Megapack 2XL',
        width: 40,
        length: 10,
      },
    ],
    [
      {
        type: 'battery',
        id: 1,
        name: 'Megapack 2XL',
        width: 40,
        length: 10,
      },
      {
        type: 'battery',
        id: 1,
        name: 'Megapack 2XL',
        width: 40,
        length: 10,
      },
    ],
    [
      {
        type: 'battery',
        id: 1,
        name: 'Megapack 2XL',
        width: 40,
        length: 10,
      },
      {
        type: 'battery',
        id: 2,
        name: 'Megapack 2',
        width: 30,
        length: 10,
      },
      {
        type: 'battery',
        id: 3,
        name: 'Megapack',
        width: 30,
        length: 10,
      },
    ],
    [
      {
        type: 'battery',
        id: 3,
        name: 'Megapack',
        width: 30,
        length: 10,
      },
      {
        type: 'transformer',
        name: 'Transformer',
        id: 1,
        width: 10,
        length: 10,
      },
      {
        type: 'transformer',
        id: 1,
        name: 'Transformer',
        width: 10,
        length: 10,
      },
    ],
  ],
};

const SiteLayout: React.FC = () => {
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
