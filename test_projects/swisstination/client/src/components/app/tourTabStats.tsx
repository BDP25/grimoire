import { h, Component } from "../../framework";
import { AmenityResponse, TourGetResponse } from "../../api/models";
import Chart from "chart.js/auto";
import { ChartOptions } from "chart.js";

interface AmenityCountChart {
  type: string;
  count: number;
}

const amenityCountOptions: ChartOptions = {
  responsive: true,
  maintainAspectRatio: false,
  animation: false,
  plugins: {
    tooltip: {
      enabled: true
    },
    legend: {
      display: false
    }
  },
  scales: {
    x: {
      ticks: { color: "#4b5563", font: { weight: "bold" } },
      grid: { drawOnChartArea: false },
      border: { color: "#4b5563" }
    },
    y: {
      beginAtZero: true,
      ticks: {
        stepSize: 1,
        color: "#4b5563",
        font: { weight: "bold" }
      },
      grid: { color: "#4b5563" },
      border: { color: "#4b5563" }
    }
  }
};

export class TourTabStats extends Component {
  // Attributes
  public tour?: TourGetResponse;

  protected componentDidMount(): void {
    this.generateAmenityCountChart();
  }

  async generateAmenityCountChart() {
    const data: AmenityCountChart[] = this.mapAmenityToCount(
      this.tour!.destination.map((dest) => dest.amenity)
    ).sort((a, b) => b.count - a.count);

    new Chart(this.shadowRoot?.querySelector("#chart") as HTMLCanvasElement, {
      type: "bar",
      options: amenityCountOptions,
      data: {
        labels: data.map((row) => row.type),
        datasets: [
          {
            label: "Count",
            data: data.map((row) => row.count),
            backgroundColor: "#B8FF9F"
          }
        ]
      }
    });
  }

  private mapAmenityToCount(elements: AmenityResponse[]): AmenityCountChart[] {
    const grouped = elements.reduce((acc, item) => {
      acc[item.amenity] = (acc[item.amenity] || 0) + 1;
      return acc;
    }, {} as Record<string, number>);

    return Object.entries(grouped).map(([type, count]) => ({ type, count }));
  }

  protected render() {
    const bgColor = "pink";
    return (
      <div className={`bg-${bgColor}-200 p-8`}>
        <h2 className="text-xl pb-4">Amenity Count of Tour</h2>
        <div className="w-full h-48">
          <canvas id="chart"></canvas>
        </div>
      </div>
    );
  }
}

customElements.define("tour-tab-stats", TourTabStats);
