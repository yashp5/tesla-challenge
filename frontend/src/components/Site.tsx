import React from 'react';
import SiteInput from './SiteInput';
import SiteDetail from './SiteDetail';
import SiteLayout from './SiteLayout';

const Site: React.FC = () => {
  return (
    <div className="flex h-screen bg-gray-100">
      <div className="w-1/3 p-4">
        <SiteInput />
      </div>
      <div className="w-2/3 p-4">
        <SiteDetail />
        <SiteLayout />
      </div>
    </div>
  );
};

export default Site;
