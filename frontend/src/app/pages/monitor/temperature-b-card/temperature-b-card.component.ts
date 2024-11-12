import { Component, OnDestroy, OnInit } from "@angular/core";
import { NbThemeService } from "@nebular/theme";
import { Subscription } from "rxjs";
import { startWith, takeWhile } from "rxjs/operators";
import { LiveUpdateChart } from "../../../@core/data/earning";
import { SocketService } from "../socket.service";

@Component({
  selector: "ngx-temperature-b-card",
  styleUrls: ["./temperature-b-card.component.scss"],
  templateUrl: "./temperature-b-card.component.html",
})
export class TemperatureBCardComponent implements OnDestroy, OnInit {
  private alive = true;

  intervalSubscription: Subscription;
  currentTheme: string;
  earningLiveUpdateCardData: LiveUpdateChart;
  liveUpdateChartData: { value: [string, number] }[];

  constructor(
    private themeService: NbThemeService,
    private socketService: SocketService
  ) {
    this.themeService
      .getJsTheme()
      .pipe(takeWhile(() => this.alive))
      .subscribe((theme) => {
        this.currentTheme = theme.name;
      });
  }

  ngOnInit() {
    this.earningLiveUpdateCardData = {
      dailyIncome: 0,
      delta: {
        up: false,
        value: 0,
      },
      liveChart: [],
    };
    let dataStorage = localStorage.getItem("temperature_humidity_data");
    this.liveUpdateChartData = dataStorage
      ? JSON.parse(dataStorage)
      : Array.from({ length: 150 }, (a, b) => {
          return {
            value: [b.toString(), 10],
          };
        });
    this.startReceivingLiveData();
  }
  startReceivingLiveData() {
    if (this.intervalSubscription) {
      this.intervalSubscription.unsubscribe();
    }

    this.intervalSubscription = this.socketService
      .getDataUpdates()
      .subscribe((res) => {
        this.earningLiveUpdateCardData = {
          ...this.earningLiveUpdateCardData,
          dailyIncome: res.data.temperature_humidity,
        };
        let temporal = [...this.liveUpdateChartData];
        temporal.push({
          value: [res.data.timestamp, res.data.temperature_humidity],
        });
        temporal.shift();
        this.liveUpdateChartData = temporal;
        localStorage.setItem("temperature_humidity_data", JSON.stringify(temporal));
        console.log(res);
      });
  }

  ngOnDestroy() {
    this.alive = false;
    this.intervalSubscription.unsubscribe();
  }
}
