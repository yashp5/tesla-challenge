import React from 'react';
import { EnergySiteDetails } from '../types/types';

interface SiteDetailProps {
  siteDetails: EnergySiteDetails;
}

const SiteDetail: React.FC<SiteDetailProps> = ({ siteDetails }) => {
  return (
    <div className="bg-white shadow-md rounded-lg p-6 mb-6 text-left">
      <h2 className="text-2xl font-bold mb-4 text-gray-800">Site Details</h2>
      <p className="text-lg text-gray-600">
        Cost: {siteDetails.cost} {siteDetails.costCurrency}
      </p>
      <p className="text-lg text-gray-600">
        Land Dimensions: {siteDetails.dimensions.width} {siteDetails.dimensions.unit} x{' '}
        {siteDetails.dimensions.length} {siteDetails.dimensions.unit}
      </p>
      <p className="text-lg text-gray-600">
        Total Energy: {siteDetails.energy} {siteDetails.energyUnit}
      </p>
      <p className="text-lg text-gray-600">
        Energy Density: {siteDetails.energyDensity} {siteDetails.energyDensityUnit}
      </p>
    </div>
  );
};

export default SiteDetail;
