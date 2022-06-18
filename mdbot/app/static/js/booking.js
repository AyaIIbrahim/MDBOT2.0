// (A) SEND BOOKING REQUEST
function book () {
  // (A1) PREVENT MULTIPLE SUBMIT
  document.getElementById("bookGo").disabled = true;

  // (A2) COLLECT FORM DATA
  let data = new FormData(document.getElementById("bookForm"));

  // (A3) SEND!
  fetch("/book", { method:"POST", body:data })
  .then((res) => {
    if (res.status==200) { location.href = "/thank"; }
    else { alert("Opps an error has occured."); }
  })
  .catch((err) => { alert("Opps an error has occured."); });
  return false;
}

// (B) ON PAGE LOAD
window.onload = () => {
  // (B1) MIN SELECTABLE DATE IS TODAY
  let datepick = document.getElementsByName("date")[0];
  datepick.min = new Date().toISOString().split("T")[0];

  // (B2) ENABLE FORM
  document.getElementById("bookGo").disabled = false;
};
