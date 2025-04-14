import { Component } from '@angular/core';

@Component({
  selector: 'app-root',
  templateUrl: './app.component.html',
  styleUrls: ['./app.component.scss']
})
export class AppComponent {
  socket!: WebSocket;
  isRecording = false;
  routes: string[] = [];
  selectedRoute!: string;
  showAutomationAlert = false;

  constructor() {
    this.initWebSocket();
  }

  initWebSocket() {
    this.socket = new WebSocket('ws://agv.local:8765');
    console.log(this.socket)

    this.socket.onopen = () => {console.log('✅ WebSocket connected'); this.sendCommand('FETCH_ROUTES')};
    this.socket.onmessage = (event) => this.handleSocketMessage(event.data);
    this.socket.onerror = (err) => console.error('❌ WebSocket error:', err);
    this.socket.onclose = () => {
      console.warn('🔁 Socket closed. Attempting reconnect...');
      setTimeout(() => this.initWebSocket(), 2000);
    };
  }

  handleSocketMessage(data: string) {
    if (data === 'HALT') {
      this.showAutomationAlert = false;
      alert('✅ Automation completed successfully!');
    } else if (data.startsWith('[')) {
      this.routes = data.replace(/[\[\]']/g, '').split(/\s*,\s*/);
      this.selectedRoute = this.routes[0];
      console.log(this.routes)
    }
  }

  sendCommand(command: string) {
    if (this.socket?.readyState === WebSocket.OPEN) {
      this.socket.send(command);
    } else {
      alert('⚠️ WebSocket not connected');
    }
  }

  toggleRecord() {
    this.isRecording = !this.isRecording;

    if (this.isRecording) {
      this.sendCommand('REC_START');
    } else {
      const pathName = prompt('Enter path name:', 'New path') || 'New path';
      const timestamp = new Date().toISOString().replace(/:/g, '-');
      this.sendCommand(`REC_STOP${pathName}~${timestamp}`);
    }
  }

  proceed() {
    if (this.selectedRoute) {
      this.sendCommand('PROCEED' + this.selectedRoute);
      this.showAutomationAlert = true;
    }
  }

  reverse() {
    if (this.selectedRoute) {
      this.sendCommand('REVERSE' + this.selectedRoute);
      this.showAutomationAlert = true;
    }
  }

  trackLine() {
    this.sendCommand('LINE');
    this.showAutomationAlert = true;
  }

  haltAutomation() {
    this.sendCommand('HALT');
    this.showAutomationAlert = false;
  }
  
}
