import { Component } from '@angular/core';

@Component({
  selector: 'app-root',
  templateUrl: './app.component.html',
  styleUrls: ['./app.component.scss']
})
export class AppComponent {
  title = 'auto-eyes';

  whitePaper() {
    window.location.href = 'https://docs.google.com/document/d/1lKIsqMYYO7nQ937QXdCg2oaPqeo0iI2x5D2HwVKsVNE/edit?usp=sharing';
  }
}
