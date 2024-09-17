import React from 'react';

const energySiteDetails = {
  cost: 600000,
  costCurrency: 'USD',
  dimensions: {
    length: 40,
    width: 100,
    unit: 'ft',
  },
  energy: 22,
  energyUnit: 'MWh',
  energyDensity: 0.0055,
  energyDensityUnit: 'MWh/sqft',
};

const SiteDetail: React.FC = () => {
  return (
    <div className="bg-white shadow-md rounded-lg p-6 mb-6 text-left">
      <h2 className="text-2xl font-bold mb-4 text-gray-800">Site Details</h2>
      <p className="text-lg text-gray-600">
        Cost: {energySiteDetails.cost} {energySiteDetails.costCurrency}
      </p>
      <p className="text-lg text-gray-600">
        Land Dimensions: {energySiteDetails.dimensions.width} {energySiteDetails.dimensions.unit} x{' '}
        {energySiteDetails.dimensions.length} {energySiteDetails.dimensions.unit}
      </p>
      <p className="text-lg text-gray-600">
        Total Energy: {energySiteDetails.energy} {energySiteDetails.energyUnit}
      </p>
      <p className="text-lg text-gray-600">
        Energy Density: {energySiteDetails.energyDensity} {energySiteDetails.energyDensityUnit}
      </p>
    </div>
  );
};

export default SiteDetail;
