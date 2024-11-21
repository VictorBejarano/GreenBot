import { Component, EventEmitter, Input, Output } from "@angular/core";

@Component({
  selector: "ngx-status-card",
  styleUrls: ["./status-card.component.scss"],
  template: `
    <nb-card (click)="click()" [ngClass]="{ off: !on }">
      <div class="icon-container">
        <div class="icon status-{{ type }}">
          <ng-content></ng-content>
        </div>
      </div>

      <div class="details">
        <div class="title h5">{{ title }}</div>
        <div class="status paragraph-2">{{ on ? "ON" : "OFF" }}</div>
      </div>
    </nb-card>
  `,
})
export class StatusCardComponent {
  @Input() title: string;
  @Input() type: string;
  @Input() id: string;
  @Input() on = true;

  @Output() onClick = new EventEmitter<any>();

  public click() {
    this.on = !this.on;
    this.onClick.emit({id: this.id, state: this.on});
  }
}
