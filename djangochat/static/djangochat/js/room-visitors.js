// static/js/room-visitors.js

//object structure used for the visitor pattern
//plain data object for each room, holding name, slug, and status
//the accept(visitor) method, which calls visitor.visitRoom(this) is the key visitor hook
class RoomElement {
  constructor({ name, status, slug }) {
    this.name   = name;
    this.status = status; // 'approved' or 'pending'
    this.slug   = slug;
  }
  accept(visitor) {
    visitor.visitRoom(this);
  }
}
//these are 2 separate operations you want to perform over exactly the same collection of rooms
//their common interface both expose a single visitRoom(room) method
class ApprovedVisitor {
  constructor(selector) { this.container = document.querySelector(selector); }
  visitRoom(room) {
    if (room.status === 'approved') {
      const btn = document.createElement('button');
      btn.textContent = room.name;
      btn.onclick   = () => location.href = `/rooms/${room.slug}/`;
      btn.className = 'px-4 py-2 m-1 bg-green-600 text-white rounded';
      this.container.appendChild(btn);
    }
  }
}

class PendingVisitor {
  constructor(selector) {
    this.container = document.querySelector(selector);
  }
  visitRoom(room) {
    if (room.status === 'pending') {
      const btn = document.createElement('button');
      btn.textContent = room.name + ' (Request)';
      btn.className   = 'px-4 py-2 m-1 bg-yellow-500 text-white rounded hover:bg-yellow-600';
      btn.style.cursor = 'pointer';
      btn.addEventListener('click', () => {
        // navigate to the room detail, which will show a Yes/No form
        window.location.href = `/rooms/${room.slug}/`;
      });
      this.container.appendChild(btn);
    }
  }
}

//the single traversal
//you loop once over your list of RoomElement objects
//each element accepts each visitor in turn, allowing that visitor to decide whether
//and how to render itself
document.addEventListener('DOMContentLoaded', () => {
  const raw        = document.getElementById('room-list').textContent;
  const roomsData  = JSON.parse(raw);
  const rooms      = roomsData.map(r => new RoomElement(r));
  const approvedV  = new ApprovedVisitor('#approved-rooms');
  const pendingV   = new PendingVisitor('#pending-rooms');

  rooms.forEach(r => { r.accept(approvedV); r.accept(pendingV); });
});

/*
Why is this the visitor pattern?
1. Separation of concerns
  - the roomElement class know only about its data(name, status, slug)
  - the 2 visitors encapsulate all the UI-rendering logic for approved vs pending status
2. Open for extendion
  - if you later need to add, say, an adminVisitor to render a 'kickuser' button for room owners
  you dont alter RoomElement
3. Single Data structure, multiple Operations
  - you have one homogeneous list (rooms). You want two distinct operations. Visitor lets you
  keep your loop and your data model DRY
 */