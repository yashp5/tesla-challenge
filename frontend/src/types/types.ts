export interface Battery {
    id: number;
    name: string;
    dimensions: {
      length: number;
      width: number;
      unit: string;
    };
    energy: number;
    energy_unit: string;
    cost: number;
    cost_currency: string;
    releaseDate: string;
    weight: number;
    weight_unit: string;
  }
  
  export interface BatterySelection {
    battery_id: number;
    quantity: number;
  }
  
  export interface EnergySiteDetails {
    cost: number;
    costCurrency: string;
    dimensions: {
      length: number;
      width: number;
      unit: string;
    };
    energy: number;
    energyUnit: string;
    energyDensity: number;
    energyDensityUnit: string;
  }
  
  export interface EnergySiteLayout {
    maxWidth: number;
    dimensions: {
      length: number;
      width: number;
      unit: string;
    };
    layout: Array<
      Array<{
        type: string;
        id: number;
        name: string;
        width: number;
        length: number;
      }>
    >;
  }