import { Injectable } from "@angular/core";
import { Observable } from "rxjs";
import { Socket } from "../../socket";

@Injectable()
export class SocketService {
  constructor(private socket: Socket) {}

  // Método para emitir datos al servidor
  sendData(event: string, data: any) {
    this.socket.emit(event, data);
  }

  // Método para recibir datos cuando el evento 'data_update' sea emitido desde el servidor
  getDataUpdates(): Observable<any> {
    return this.socket.fromEvent("data_update");
  }
}
