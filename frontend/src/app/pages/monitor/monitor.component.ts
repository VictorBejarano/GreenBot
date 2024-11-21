import { Component } from "@angular/core";
import { SocketService } from "./socket.service";
import { Socket } from "../../socket";
import { CsvService } from "./csv.service";
import { take } from "rxjs-compat/operator/take";

@Component({
  selector: "ngx-monitor",
  styleUrls: ["./monitor.component.scss"],
  templateUrl: "./monitor.component.html",
})
export class MonitorComponent {
  statusCards = [
    {
      title: "Light",
      iconClass: "nb-lightbulb",
      type: "warning",
      id: "fan",
    },
    {
      title: "Fan",
      iconClass: "nb-loop",
      type: "success",
      id: "luz",
    },
  ];
  /**
   *
   */
  constructor(private service: SocketService, private csvService: CsvService) {
    this.service.sendData("get_last_150_data", "");
  }

  setActuator(input: any) {
    if (input.id === "fan" && input.state)
      this.service.sendData("activate_fan", "");
    if (input.id === "fan" && !input.state)
      this.service.sendData("desactivate_fan", "");
    if (input.id === "luz" && input.state)
      this.service.sendData("activate_luz", "");
    if (input.id === "luz" && !input.state)
      this.service.sendData("desactivate_luz", "");
  }

  download() {
    this.service.sendData("get_last_150_data", "");
    const subscription = this.service
      .getAllData()
      .pipe()
      .subscribe((res) => {
        this.csvService.exportToCsv(res.data, "data_export");
        subscription.unsubscribe()
      });
  }
}
