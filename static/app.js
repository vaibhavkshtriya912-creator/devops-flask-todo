document.getElementById("todoForm").addEventListener("submit", async (e) => {
  e.preventDefault();
  const payload = {
    itemName: document.getElementById("itemName").value.trim(),
    itemDescription: document.getElementById("itemDescription").value.trim(),
  };
  const adv = document.getElementById("advancedFields");
  if (adv && !adv.classList.contains("hidden")) {
    const idEl = document.getElementById("itemId");
    const uuidEl = document.getElementById("itemUuid");
    const hashEl = document.getElementById("itemHash");
    if (idEl && idEl.value) payload.itemId = idEl.value;
    if (uuidEl && uuidEl.value) payload.itemUuid = uuidEl.value;
    if (hashEl && hashEl.value) payload.itemHash = hashEl.value;
  }
  const res = await fetch("/submittodoitem", {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify(payload),
  });
  const data = await res.json();
  document.getElementById("result").textContent = JSON.stringify(data, null, 2);
});
