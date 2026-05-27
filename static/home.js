function switchUser() {
    document.querySelector(".active").classList.remove("active");
    document.getElementById("user-button").classList.add("active");
    document.getElementsByClassName("business-form")[0].style.display = 'none';
    document.getElementsByClassName("user-form")[0].style.display = 'flex';
}

function switchBusiness() {
    document.querySelector(".active").classList.remove("active")
    document.getElementById("business-button").classList.add("active");
    document.getElementsByClassName("user-form")[0].style.display = 'none';
    document.getElementsByClassName("business-form")[0].style.display = 'flex';
}

async function getResponse(path, formData) {
    const response = await fetch(path, {
        method: "POST",
        body: formData,
        });

    return await response.json();
}

function createTuple(row, b = false) {
    const tuple = row.split(",");
    const node = document.createElement("div");
    node.classList.add("u-tuple");
    if (b) node.classList.add("ref");
    for (const col of tuple) {
        p = document.createElement("p");
        p.textContent = col;
        node.appendChild(p);
    }
    document.querySelector(".tuple-list").appendChild(node);
}

async function submitSearch(form) {
    const placeholder = document.querySelector(".placeholder");
    const placeholderText = document.querySelector(".placeholder p");
    const placeholderImg = document.querySelector(".placeholder img");
    const footerText = document.querySelector(".footer p");
    const tupleList = document.querySelector(".tuple-list");
    placeholderText.style.display = "none";
    tupleList.style.display = "none";
    tupleList.textContent = "";
    placeholderImg.style.display = "block";
    placeholder.style.display = "flex";
    try {
        const formData = new FormData(form);
        formData.append("query_type", form.id);
        if (form.id == "user-search") {
            tupleList.style.gridTemplateColumns = "repeat(8, 1fr)";
            createTuple("user_id,name,review_count,useful,funny,cool,average_stars,yelping_since", true);
            // clean and validate user input on business searches
            if (formData.get("u_review_count") == "") formData.set("u_review_count", 0);
            if (formData.get("u_stars") == "") formData.set("u_stars", 1);
            if (formData.get("u_review_count") < 0) {
                throw new Error("Invalid review count entered.");
            }
            if (formData.get("u_stars") > 5 || formData.get("u_stars") < 1) {
                throw new Error("Invalid star value entered.");
            }
        } else if (form.id == "business-search") {
            tupleList.style.gridTemplateColumns = "repeat(5, 1fr)";
            createTuple("business_id,name,address,city,stars", true);
            // clean and validate user input on user searches
            if (formData.get("b_stars") == "") formData.set("b_stars", 1);
            if (formData.get("b_stars") > 5 || formData.get("b_stars") < 1) {
                throw new Error("Invalid star value entered.");
            }
        }
        // send POST request
        const path = "/query";
        const data = await getResponse(path, formData);

        footerText.innerHTML = `${data.length} results.`
        if (data == "-1") throw new Error("Query failed.");
        if (data.length == 0) throw new Error("No results found.");
        for (const row of data) {
            createTuple(row);
        }
        placeholderImg.style.display = "none";
        placeholder.style.display = "none";
        tupleList.style.display = "grid";

    } catch (e) {
        tupleList.style.display = "none";
        placeholderImg.style.display = "none";
        placeholderText.style.display = "block";
        placeholderText.textContent = e
        footerText.textContent = "0 results."
        console.error(e);
    }
}

async function submitInsertion(form)  {
    const dialog = document.querySelector("#dialog");
    const dialogContent = dialog.querySelector('p');
    try {
        const formData = new FormData(form);
        formData.append("query_type", form.id);
        console.log(form.id)
        if (form.id == "add-review") {
            // validate data for review
            if (formData.get("r_stars") > 5 || formData.get("r_stars") < 1) {
                throw new Error("Invalid star value entered.");
            }
        }

        const path = "/insert";
        const data = await getResponse(path, formData);

        dialogContent.textContent = data.msg;
    } catch (e) {
        dialogContent.textContent = `Error: ${e}`
    }
    dialog.showModal();
}

function selectTuple(event) {
    const actionTab = document.querySelector(".action");
    const homeTab = document.querySelector(".home");
    target = event.target;
    if (target.nodeName == "P")
        target = event.target.parentNode;
    if (target.classList.contains("selected")) {
        target.classList.remove("selected");
        actionTab.style.display = "none";
        homeTab.style.display = "flex";
        return
    }
    if (target.classList.contains("u-tuple") && !target.classList.contains("ref")) {
        document.querySelector(".selected")?.classList.remove("selected");
        target.classList.add("selected");

        const id = target.firstChild.textContent;
        const id_type = document.querySelector(".u-tuple p").innerHTML;
        // first form is the form we want to show
        const forms = (id_type == "user_id") ? [".friend-form", ".review-form"] : [".review-form", ".friend-form"];
        document.querySelector(forms[1]).style.display = "none";
        document.querySelector(forms[0]).style.display = "flex";
        
        document.querySelector(`${forms[0]} form input`).value = id;
        console.log(document.querySelector(`${forms[0]} form input`))
        homeTab.style.display = "none";
        actionTab.style.display = "flex";
    }
}

document.addEventListener("DOMContentLoaded", () => {
    document.getElementById("user-button").addEventListener("click", switchUser);
    document.getElementById("business-button").addEventListener("click", switchBusiness);
    document.querySelector(".tuple-list").addEventListener("click", (e)=>{selectTuple(e)});
    const userForm = document.getElementById("user-search");
    const businessForm = document.getElementById("business-search");
    const friendForm = document.getElementById("add-friend");
    const reviewForm = document.getElementById("add-review");

    userForm.addEventListener("submit", (event)=>{event.preventDefault();submitSearch(userForm)});
    businessForm.addEventListener("submit", (event)=>{event.preventDefault();submitSearch(businessForm)});
    friendForm.addEventListener("submit", (event)=>{event.preventDefault();submitInsertion(friendForm)});
    reviewForm.addEventListener("submit", (event)=>{event.preventDefault();submitInsertion(reviewForm)});
});