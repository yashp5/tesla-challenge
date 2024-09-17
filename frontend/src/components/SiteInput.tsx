import React from 'react';

const batteryData = [
  {
    id: 1,
    name: 'Megapack 2XL',
    dimensions: {
      length: 40,
      width: 10,
      unit: 'ft',
    },
    energy: 4,
    energy_unit: 'MWh',
    cost: 120000,
    cost_currency: 'USD',
    releaseDate: '2022-01-01',
    weight: 40000,
    weight_unit: 'kg',
  },
  {
    id: 2,
    name: 'Megapack 2',
    dimensions: {
      length: 30,
      width: 10,
      unit: 'ft',
    },
    energy: 3,
    energy_unit: 'MWh',
    cost: 80000,
    cost_currency: 'USD',
    releaseDate: '2021-03-15',
    weight: 35000,
    weight_unit: 'kg',
  },
  {
    id: 3,
    name: 'Megapack',
    dimensions: {
      length: 30,
      width: 10,
      unit: 'ft',
    },
    energy: 2,
    energy_unit: 'MWh',
    cost: 50000,
    cost_currency: 'USD',
    releaseDate: '2005-06-30',
    weight: 30000,
    weight_unit: 'kg',
  },
  {
    id: 4,
    name: 'Powerpack',
    dimensions: {
      length: 10,
      width: 10,
      unit: 'ft',
    },
    energy: 1,
    energy_unit: 'MWh',
    cost: 20000,
    cost_currency: 'USD',
    releaseDate: '2000-12-01',
    weight: 15000,
    weight_unit: 'kg',
  },
];

const SiteInput: React.FC = () => {
  return (
    <div className="bg-white shadow-md rounded-lg p-6 text-left">
      <h2 className="text-2xl font-bold mb-6 text-gray-800">Select Batteries</h2>
      {batteryData.map((battery) => (
        <div key={battery.name} className="mb-4 grid grid-cols-2 gap-4">
          <label className="text-base font-large text-gray-700">{battery.name}:</label>
          <input
            type="number"
            min="0"
            defaultValue="0"
            className="w-full px-3 py-2 text-gray-700 bg-gray-100 rounded-md border border-gray-300 
                       focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-transparent
                       transition duration-200 ease-in-out"
          />
        </div>
      ))}
      <button
        className="mt-6 w-full bg-blue-500 hover:bg-blue-600 text-white font-bold py-2 px-4 rounded
                   transition duration-200 ease-in-out focus:outline-none focus:ring-2 
                   focus:ring-blue-500 focus:ring-opacity-50">
        Build Layout
      </button>
    </div>
  );
};

export default SiteInput;
