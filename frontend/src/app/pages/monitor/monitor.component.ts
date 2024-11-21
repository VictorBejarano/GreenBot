import { Component } from "@angular/core";
import { SocketService } from "./socket.service";
import { Socket } from "../../socket";

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
      type: "primary",
      id: 'fan'
    },
    {
      title: "Light",
      iconClass: "nb-lightbulb",
      type: "primary",
      id: 'luz'
    },
  ];
  /**
   *
   */
  constructor(private service: SocketService) {
    this.service.sendData("get_last_150_data", "");
  }

  setActuator(input: any) {
    if(input.id === 'fan' && input.state)
      this.service.sendData("activate_fan", "");
    if(input.id === 'fan' && !input.state)
      this.service.sendData("desactivate_fan", "");
    if(input.id === 'luz' && input.state)
      this.service.sendData("activate_luz", "");
    if(input.id === 'luz' && !input.state)
      this.service.sendData("desactivate_luz", "");

  }
}
