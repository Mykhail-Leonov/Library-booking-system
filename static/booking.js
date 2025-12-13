// Booths in each building
const BOOTHS = {
  "David Hockney": ["DHB A - Capacity: 6", "DHB B - Capacity: 4", "DHB C - Capacity: 4", "DHB D - Capacity: 4"],
  "TG": ["TG 1 - Capacity: 4", "TG 2 - Capacity: 4", "TG 3 - Capacity: 4"]
};

const BOOTH_IMAGES = {
  "DHB A - Capacity: 6": "/static/booth-images/DHB_A.jpg",
  "DHB B - Capacity: 4": "/static/booth-images/DHB_B.jpg",
  "DHB C - Capacity: 4": "/static/booth-images/DHB_C.jpg",
  "DHB D - Capacity: 4": "/static/booth-images/DHB_D.jpg",
  "TG 1 - Capacity: 4": "/static/booth-images/TG_1.jpg",
  "TG 2 - Capacity: 4": "/static/booth-images/TG_2.jpg",
  "TG 3 - Capacity: 4": "/static/booth-images/TG_3.jpg"
};

let selectedBuilding = "";

let selectedBooth = "";

let selectedDate = "";

const monthView = new Date();
monthView.setDate(1);

function $(id) {
  return document.getElementById(id);
}

function getUser() {
  return JSON.parse(localStorage.getItem("user"));
}

function toISODate(date) {
  return date.toISOString().split("T")[0];
}

/* Buildings and booths */

$("buildingSelect").addEventListener("change", function () {
  selectedBuilding = this.value;
  selectedBooth = "";
  selectedDate = "";

  $("boothList").innerHTML = "";
  $("Calendar-grid").innerHTML = "";
  $("slotsBox").innerHTML = "";

  BOOTHS[selectedBuilding].forEach(function (booth) {
    const btn = document.createElement("button");
    btn.className = "booth-btn";
    btn.textContent = booth;

    btn.onclick = function () {
      selectedBooth = booth;
      showBoothImage(booth);

      document.querySelectorAll(".booth-btn").forEach(b =>
        b.classList.remove("active")
      );
      btn.classList.add("active");

      loadMonth();
    };

    $("boothList").appendChild(btn);
  });
});

/* Booths images */
function showBoothImage(booth) {
  const img = document.getElementById("boothImage");
  const src = BOOTH_IMAGES[booth];

  if (!src) {
    img.style.display = "none";
    return;
  }

  img.src = src;
  img.alt = `Image of booth ${booth}`;
  img.style.display = "block";
}




/*Calendar */

function loadMonth() {
  fetch(`/api/bookings/month?booth=${selectedBooth}&year=${monthView.getFullYear()}&month=${monthView.getMonth() + 1}`)
    .then(res => res.json())
    .then(data => renderCalendar(data));
}

function renderCalendar(data) {
  $("MonthLabel").textContent =
    monthView.toLocaleDateString(undefined, { month: "long", year: "numeric" });

  const grid = $("Calendar-grid");
  grid.innerHTML = "";
  $("slotsBox").innerHTML = "";

  const allowed = new Set(data.allowed_dates);
  const summary = data.summary;
  const totalSlots = data.total_slots;

  const firstDay = new Date(monthView.getFullYear(), monthView.getMonth(), 1);
  const offset = (firstDay.getDay() + 6) % 7;
  const daysInMonth = new Date(monthView.getFullYear(), monthView.getMonth() + 1, 0).getDate();

  for (let i = 0; i < offset; i++) {
    grid.appendChild(document.createElement("div"));
  }

  for (let day = 1; day <= daysInMonth; day++) {
    const dateObj = new Date(monthView.getFullYear(), monthView.getMonth(), day);
    const dateStr = toISODate(dateObj);

    const cell = document.createElement("button");
    cell.className = "cal-cell day";
    cell.textContent = day;

    if (!allowed.has(dateStr)) {
      cell.classList.add("off");
      cell.disabled = true;
    } else {
      const count = summary[dateStr] || 0;

      if (count === 0) cell.classList.add("free");
      else if (count >= totalSlots) {
        cell.classList.add("full");
        cell.disabled = true;
      } else cell.classList.add("partial");

      cell.onclick = function () {
        document.querySelectorAll(".sel").forEach(d =>
          d.classList.remove("sel")
        );
        cell.classList.add("sel");

        selectedDate = dateStr;
        loadSlots();
      };
    }

    grid.appendChild(cell);
  }
}

/* Time slots */

function loadSlots() {
  fetch(`/api/bookings/slots?booth=${selectedBooth}&date=${selectedDate}`)
    .then(res => res.json())
    .then(data => {
      const box = $("slotsBox");
      box.innerHTML = "";

      data.time_slots.forEach(function (slot) {
        const btn = document.createElement("button");
        btn.className = "slot-btn";
        btn.textContent = slot;

        if (data.booked_slots.includes(slot)) {
          btn.disabled = true;
        } else {
          btn.onclick = function () {
            bookSlot(slot);
          };
        }

        box.appendChild(btn);
      });
    });
}

/* Booking */

function bookSlot(slot) {
  const user = getUser();

  if (!user) {
    alert("Please log in to book.");
    window.location.href = "/login";
    return;
  }

  fetch("/api/bookings", {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({
      user_id: user.id,
      building: selectedBuilding,
      booth: selectedBooth,
      date: selectedDate,
      time_slot: slot
    })
  })
    .then(res => res.json())
    .then(data => {
      if (data.error) alert(data.error);
      else alert(data.message);

      loadMonth();
      loadSlots();
    });
}

/* Month navigation */

$("PreviousMonthButton").onclick = function () {
  monthView.setMonth(monthView.getMonth() - 1);
  loadMonth();
};

$("NextMonthButton").onclick = function () {
  monthView.setMonth(monthView.getMonth() + 1);
  loadMonth();
};
