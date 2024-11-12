import { NgModule } from "@angular/core";
import { MonitorComponent } from "./monitor.component";
import { TemperatureCardComponent } from "./temperature-card/temperature-card.component";
import { TemperatureLiveUpdateChartComponent } from "./temperature-card/temperature-live-update-chart.component";
import { NbCardModule, NbIconModule, NbSelectModule } from "@nebular/theme";
import { ThemeModule } from "../../@theme/theme.module";
import { NgxEchartsModule } from "ngx-echarts";
import { SocketService } from "./socket.service";

import { SocketIoConfig } from "../../socket/config/socket-io.config";
import { SocketIoModule } from "../../socket";
import { HumidityCardComponent } from "./humidity-card/humidity-card.component";
import { SoilMoistureCardComponent } from "./soil-moisture-card/soil-moisture-card.component";
import { TemperatureBCardComponent } from "./temperature-b-card/temperature-b-card.component";
import { QualityCardComponent } from "./quality-card/quality-card.component";
const config: SocketIoConfig = { url: "http://192.168.10.3:5000", options: {} };

@NgModule({
  imports: [
    ThemeModule,
    NbIconModule,
    NbCardModule,
    NbSelectModule,
    NgxEchartsModule,
    SocketIoModule.forRoot(config),
  ],
  declarations: [
    MonitorComponent,
    TemperatureCardComponent,
    TemperatureLiveUpdateChartComponent,
    HumidityCardComponent,
    SoilMoistureCardComponent,
    TemperatureBCardComponent,
    QualityCardComponent,
  ],
  providers: [SocketService],
})
export class MonitorModule {}
