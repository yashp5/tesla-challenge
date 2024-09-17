import React from 'react';
import SiteDetail from './SiteDetail';
import SiteLayout from './SiteLayout';
import { useState, useEffect, FormEvent } from 'react';
import { Battery, EnergySiteDetails, EnergySiteLayout, BatterySelection } from '../types/types';

const Site: React.FC = () => {
  const [batteries, setBatteries] = useState<Battery[]>([]);
  const [siteDetails, setSiteDetails] = useState<EnergySiteDetails | null>(null);
  const [siteLayout, setSiteLayout] = useState<EnergySiteLayout | null>(null);

  useEffect(() => {
    const fetchBatteries = async () => {
      try {
        const response = await fetch('http://localhost:9000/data/batteries');
        if (!response.ok) {
          throw new Error('Failed to fetch batteries');
        }
        const data = await response.json();
        setBatteries(data);
      } catch (error) {
        console.error('Error fetching batteries:', error);
      }
    };

    fetchBatteries();
  }, []);

  const handleBuildLayout = async (e: FormEvent) => {
    e.preventDefault();
    const form = e.target as HTMLFormElement;
    const batterySelections: BatterySelection[] = batteries
      .map((battery) => ({
        batteryId: battery.id,
        quantity: parseInt(form[`battery-${battery.id}`].value, 10) || 0,
      }))
      .filter((selection) => selection.quantity > 0);

    try {
      const response = await fetch('http://localhost:9000/site/build', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
          accept: 'application/json',
        },
        body: JSON.stringify(batterySelections),
      });

      if (!response.ok) {
        throw new Error('Failed to build layout');
      }

      const data = await response.json();
      const energySiteDetails: EnergySiteDetails = {
        cost: data.cost,
        costCurrency: data.costCurrency,
        dimensions: data.dimensions,
        energy: data.energy,
        energyUnit: data.energyUnit,
        energyDensity: Number(Number(data.energyDensity).toFixed(4)),
        energyDensityUnit: data.energyDensityUnit,
      };
      const energySiteLayout: EnergySiteLayout = {
        maxWidth: data.maxWidth,
        dimensions: data.dimensions,
        layout: data.layout,
      };
      setSiteDetails(energySiteDetails);
      setSiteLayout(energySiteLayout);
    } catch (error) {
      console.error('Error building layout:', error);
    }
  };

  return (
    <div className="flex h-screen bg-gray-100">
      <div className="w-1/3 p-4">
        <form onSubmit={handleBuildLayout} className="bg-white shadow-md rounded-lg p-6 text-left">
          <h2 className="text-2xl font-bold mb-6 text-gray-800">Select Batteries</h2>
          {batteries.map((battery) => (
            <div key={battery.id} className="mb-4 grid grid-cols-2 gap-4">
              <label className="text-base font-large text-gray-700">{battery.name}:</label>
              <input
                type="number"
                min="0"
                defaultValue="0"
                name={`battery-${battery.id}`}
                className="w-full px-3 py-2 text-gray-700 bg-gray-100 rounded-md border border-gray-300 
                       focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-transparent
                       transition duration-200 ease-in-out"
              />
            </div>
          ))}
          <button
            type="submit"
            className="mt-6 w-full bg-blue-500 hover:bg-blue-600 text-white font-bold py-2 px-4 rounded
                   transition duration-200 ease-in-out focus:outline-none focus:ring-2 
                   focus:ring-blue-500 focus:ring-opacity-50">
            Build Layout
          </button>
        </form>
      </div>
      <div className="w-2/3 p-4">
        {siteDetails && <SiteDetail siteDetails={siteDetails} />}
        {siteLayout && <SiteLayout energySiteLayout={siteLayout} />}
      </div>
    </div>
  );
};

export default Site;
