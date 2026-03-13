
// Identificar custom items usados en el latex

const customItems = Array.from(document.querySelectorAll("li")).filter(
  li => li.innerHTML?.includes("adhocprefix")
)

for (const customItem of customItems) {

  // quitar el texto que identifica al custom item
  //customItem.innerHTML = customItem.innerHTML?.replace(/adhocprefix.*adhocsufix/, "") ?? ""

  // quitar marker original
  customItem.classList.add("no-marker");
}

document.body.innerHTML = document.body.innerHTML.replaceAll(/adhocprefix|adhocsufix/g, "")
