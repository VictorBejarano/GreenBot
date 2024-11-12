import { Component, OnDestroy, OnInit } from "@angular/core";
import { SocketService } from "./socket.service";
import { Socket } from "../../socket";

@Component({
  selector: "ngx-monitor",
  styleUrls: ["./monitor.component.scss"],
  templateUrl: "./monitor.component.html",
})
export class MonitorComponent implements OnInit, OnDestroy {
  data: any;

  constructor(private socket: Socket) {}

  ngOnInit() {
    // // Escuchar el evento 'data_update' del servidor Flask
    // this.socket
    //   .fromEvent("data_update")
    //   .subscribe((data) => {
    //     console.log("Datos recibidos:", data);
    //     this.data = data;
    //   });

    // // Emitir un evento de ejemplo
    // this.socket.emit('start_bluetooth_stream', '');
  }

  ngOnDestroy() {
  }
}
