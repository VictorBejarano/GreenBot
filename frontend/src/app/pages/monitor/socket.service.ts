// src/app/socket.service.ts
import { Injectable } from "@angular/core";
import { io, Socket } from "socket.io-client";
import { Observable } from "rxjs";

@Injectable()
export class SocketService {
  private socket: Socket;

  constructor() {
    // Cambia la URL por la dirección de tu servidor Flask
    this.socket = io("http://192.168.10.3:5000");
  }

  // Método para escuchar eventos desde el servidor
  listen(eventName: string): Observable<any> {
    return new Observable((subscriber) => {
      this.socket.on(eventName, (data) => {
        subscriber.next(data);
      });
    });
  }

  // Método para emitir eventos al servidor
  emit(eventName: string, data: any) {
    this.socket.emit(eventName, data);
  }

  // Método para desconectar el socket
  disconnect() {
    this.socket.disconnect();
  }
}
