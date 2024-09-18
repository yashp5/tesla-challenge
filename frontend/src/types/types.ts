export interface Battery {
  id: number;
  name: string;
  dimensions: {
    length: number;
    width: number;
    unit: string;
  };
  energy: number;
  energyUnit: string;
  cost: number;
  costCurrency: string;
  releaseDate: string;
  weight: number;
  weightUnit: string;
  color: string;
}

export interface Transformer {
  id: number;
  name: string;
  dimensions: {
    length: number;
    width: number;
    unit: string;
  };
  energy: number;
  energyUnit: string;
  cost: number;
  costCurrency: string;
  releaseDate: string;
  weight: number;
  weightUnit: string;
  color: string;
}

export interface BatterySelection {
  batteryId: number;
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
