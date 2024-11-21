import { Component } from "@angular/core";
import { SocketService } from "./socket.service";
import { Socket } from "../../socket";

@Component({
  selector: "ngx-monitor",
  styleUrls: ["./monitor.component.scss"],
  templateUrl: "./monitor.component.html",
})
export class MonitorComponent {
  /**
   *
   */
  constructor(private service: SocketService) {
    this.service.sendData("get_last_150_data", "");
  }
}
