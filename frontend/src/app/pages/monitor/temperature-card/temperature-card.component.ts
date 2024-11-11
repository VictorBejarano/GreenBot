import { Component, Input, OnDestroy, OnInit } from "@angular/core";
import { NbThemeService } from "@nebular/theme";
import { interval, Subscription } from "rxjs";
import { switchMap, takeWhile } from "rxjs/operators";
import { LiveUpdateChart, EarningData } from "../../../@core/data/earning";

@Component({
  selector: "ngx-temperature-card",
  styleUrls: ["./temperature-card.component.scss"],
  templateUrl: "./temperature-card.component.html",
})
export class TemperatureCardComponent implements OnDestroy, OnInit {
  private alive = true;

  intervalSubscription: Subscription;
  currentTheme: string;
  earningLiveUpdateCardData: LiveUpdateChart;
  liveUpdateChartData: { value: [string, number] }[];

  constructor(
    private themeService: NbThemeService,
    private earningService: EarningData
  ) {
    this.themeService
      .getJsTheme()
      .pipe(takeWhile(() => this.alive))
      .subscribe((theme) => {
        this.currentTheme = theme.name;
      });
  }

  ngOnInit() {
    this.getEarningCardData('Bitcoin');
  }

  private getEarningCardData(currency) {
    this.earningService
      .getEarningCardData(currency)
      .pipe(takeWhile(() => this.alive))
      .subscribe((earningLiveUpdateCardData: LiveUpdateChart) => {
        this.earningLiveUpdateCardData = earningLiveUpdateCardData;
        this.liveUpdateChartData = earningLiveUpdateCardData.liveChart;

        this.startReceivingLiveData(currency);
      });
  }

  startReceivingLiveData(currency) {
    if (this.intervalSubscription) {
      this.intervalSubscription.unsubscribe();
    }

    this.intervalSubscription = interval(200)
      .pipe(
        takeWhile(() => this.alive),
        switchMap(() =>
          this.earningService.getEarningLiveUpdateCardData(currency)
        )
      )
      .subscribe((liveUpdateChartData: any[]) => {
        this.liveUpdateChartData = [...liveUpdateChartData];
      });
  }

  ngOnDestroy() {
    this.alive = false;
  }
}
