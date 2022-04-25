import { defineStore } from "pinia";
import type { DataPoint } from "@/models/datapoint.model";

export type RootState = {
  data: DataPoint[];
};

const getDataPoints = async (): Promise<DataPoint[]> => {
  const res = await fetch("http://localhost:5000/data");
  const json = await res.json();
  return json.data;
};

export const useDataStore = defineStore("data", {
  state: () =>
    ({
      data: [],
    } as RootState),
  actions: {
    async fetchData() {
      try {
        const data = await getDataPoints();
        this.data = data;
      } catch (e) {
        console.error(e);
      }
    },
  },
});
