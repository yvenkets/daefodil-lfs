const body = document.querySelector("body");


sidebar = body.querySelector(".sidebar"),
  toggle = body.querySelector(".toggle");
let button = document.querySelector(".menu-icon");
link = document.querySelector(".mobile-sidebar");

toggle.addEventListener("click", () => {
  sidebar.classList.toggle("close");
  toggle.classList.toggle("collapse");
});

function openNav() {
  document.getElementById("mob-sidebar").style.width = "320px";
}
function closeNav() {
  document.getElementById("mob-sidebar").style.width = "0%";
}

button.addEventListener("click", () => {
  link.classList.toggle("display");
});


$(".menu ul li a").click(function () {

  var id = $(this).attr("id");
  console.log(id);
  $("nav ul .item-show-" + id).toggleClass("show");
  $("nav ul li #" + id + " svg").toggleClass("rotate");
});
$(".menu ul li").click(function () {

  $(this).addClass("active").siblings().removeClass("active");
  $(this).siblings().children().removeClass("show");
  $(this).siblings().children().children().removeClass("rotate");
  $(this).siblings().children().children().removeClass("sub_active");
});
$(".menu ul li .item-show-1 a").click(function () {
  $(this).addClass("sub_active").siblings().removeClass("sub_active");
});


// tabs

$(".tabContent").hide();
$("ul.tabs li:first").addClass("active").show();
$(".tabContent:first").show();

$("ul.tabs li").click(function () {
  $("ul.tabs li").removeClass("active");
  $(this).addClass("active");
  $(".tabContent").hide();
  var activeTab = $(this).find("a").attr("href");
  $(activeTab).fadeIn();
  return false;
});



var $table = document.getElementById("myTable"),
  $n = 5,
  $rowCount = $table.rows.length,
  $firstRow = $table.rows[0].firstElementChild.tagName,
  $hasHead = ($firstRow === "TH"),
  $tr = [],
  $i, $ii, $j = ($hasHead) ? 1 : 0,
  $th = ($hasHead ? $table.rows[(0)].outerHTML : "");
var $pageCount = Math.ceil($rowCount / $n);
if ($pageCount > 1) {
  for ($i = $j, $ii = 0; $i < $rowCount; $i++, $ii++)
    $tr[$ii] = $table.rows[$i].outerHTML;
  $table.insertAdjacentHTML("afterend", "<div id='buttons' style='text-align:end;'></div");
  sort(1);
}

function sort($p) {
  var $rows = $th, $s = (($n * $p) - $n);
  for ($i = $s; $i < ($s + $n) && $i < $tr.length; $i++)
    $rows += $tr[$i];

  $table.innerHTML = $rows;
  document.getElementById("buttons").innerHTML = pageButtons($pageCount, $p);
  document.getElementById("id" + $p).setAttribute("class", "page_active");
}


function pageButtons($pCount, $cur) {
  var $prevDis = ($cur == 1) ? "disabled" : "",
    $nextDis = ($cur == $pCount) ? "disabled" : "",
    $buttons = "<input type='button' value='<' onclick='sort(" + ($cur - 1) + ")' " + $prevDis + ">";
  for ($i = 1; $i <= $pCount; $i++)
    $buttons += "<input type='button' id='id" + $i + "'value='" + $i + "' onclick='sort(" + $i + ")'>";
  $buttons += "<input type='button' value='>' onclick='sort(" + ($cur + 1) + ")' " + $nextDis + ">";
  return $buttons;
}

function toggleDropdown() {
  var dropdown = document.getElementById("dropdown");
  if (dropdown.style.display === "block") {
    dropdown.style.display = "none";
  } else {
    dropdown.style.display = "block";
  }
}


// // Get the URL of the current page
// var currentUrl = window.location.href;

// // Get all li elements with a class of "nav-link"
// var navLinks = document.querySelectorAll('.nav-link');

// // Loop through the navLinks array and check if the href attribute matches the current URL
// for (var i = 0; i < navLinks.length; i++) {
//   var link = navLinks[i].querySelector('a');
//   if (link.getAttribute('href') === currentUrl) {
//     navLinks[i].classList.add('active');
//   } else {
//     navLinks[i].classList.remove('active');
//   }
// }



function loadPage() {

  var myItem = localStorage.getItem('dropdownWasOpen');
  let pageurl
  //alert(myItem)

  if (myItem) {
    //alert("dropdown")
    $(".menu ul li").trigger("click");
    $(".menu ul li a").trigger("click");
  }
  //$(window).bind('load', function() {
  //alert('inside')
  // Get the URL of the current page
  // alert(document.querySelectorAll('.nav-link'))
  var currentUrl = location.pathname;

  // Get all li elements with a class of "nav-link"
  var navLinks = document.querySelectorAll('.nav-link');

  console.log('location', currentUrl, navLinks)

  // Loop through the navLinks array and check if the href attribute matches the current URL

  for (var i = 0; i < navLinks.length; i++) {
    //alert(i)
    var link = navLinks[i].querySelector('a');
    //alert(link)
    if (link.getAttribute('href') === currentUrl) {
      //alert('insideif')
      navLinks[i].classList.add('active');
      if (navLinks[i] && navLinks[i].closest('.nav-link.parentDiv')) {
        navLinks[i].closest('.nav-link.parentDiv').classList.add('active');
        navLinks[i].closest('.item-show-1').classList.add('show');
      }

    } else {
      navLinks[i].classList.remove('active');
    }
  }
  var menuLinks = document.querySelectorAll('.submenu-link');

for (var i = 0; i < menuLinks.length; i++) {
  //alert(i)
  var link = menuLinks[i].querySelector('a');
  //alert(link)
  if (link.getAttribute('href') === currentUrl) {
    //alert('insideif')
    menuLinks[i].classList.add('active');

  } else {
    menuLinks[i].classList.remove('active');
  }
}

}


// Get all li elements with a class of "nav-link"

function testing() {
  var currentURL = window.location.href;
  alert(currentURL)
  if (currentURL === "http://localhost:8023/preview") {
      var listItems = document.querySelectorAll("#myList li");
      for (var i = 0; i < listItems.length; i++) {
          var listItem = listItems[i];
          listItem.classList.add("disabled");
          listItem.querySelector("a").setAttribute("disabled", true);
      }
  }
};





//new-one
let myVariable = 0;

function test() {
  //alert("String")

  myVariable = 1 - myVariable


  if (myVariable == 1) {
    //alert("True")
    localStorage.setItem("dropdownWasOpen", "true");
  } else {
    //alert("False")
    localStorage.removeItem("dropdownWasOpen");
  }
  // let myVariable = localStorage.getItem('dropdownWasOpen') === 'true' || false;
  // const myVariableValueElement = document.getElementById('');
  // myVariableValueElement.textContent = myVariable.toString();
  // const toggleButton = document.getElementById('toggle-button');

  // toggleButton.addEventListener('click', () => {
  //   myVariable = !myVariable;
  //   localStorage.setItem('dropdownWasOpen', myVariable.toString());
  //   myVariableValueElement.textContent = myVariable.toString();
  // });
}


// function urlstay(){
//   alert('inside')
//   // Get the URL of the current page
//   // alert(document.querySelectorAll('.nav-link'))
//   var currentUrl = location.pathname;

//   // Get all li elements with a class of "nav-link"
//   var navLinks = document.querySelectorAll('.nav-link');

//   console.log('location', currentUrl, navLinks)

//   // Loop through the navLinks array and check if the href attribute matches the current URL

//   for (var i = 0; i < navLinks.length; i++) {

//     var link = navLinks[i].querySelector('a');
//     we=link.getAttribute('href') === currentUrl
//     alert(currentUrl)
//     alert(link.getAttribute('href'))
//     alert(we)
//     if (link.getAttribute('href') === currentUrl) {
//       //alert('insideif')
//       navLinks[i].classList.add('active');

//     } else {
//       navLinks[i].classList.remove('active');
//     }
//   }

// }

// window.onload = function() {
// alert('inside')
// // Get the current URL
// const currentUrl = window.location.href;

// // Get all menu items
// const menuItems = document.querySelectorAll('.nav-link');

// // Loop through menu items
// menuItems.forEach(item => {
//   // Get the URL of the menu item
//   const itemUrl = item.href;

//   // Check if the current URL matches the menu item URL
//   if (currentUrl === itemUrl) {
//     // Add the "active" class to the menu item
//     item.classList.add('active');

//     // Check if the menu item has a parent menu item
//     const parentMenuItem = item.closest('.nav-link');
//     if (parentMenuItem) {
//       // Add the "active" class to the parent menu item
//       parentMenuItem.classList.add('active');
//     }
//   } else {
//     // Remove the "active" class from the menu item
//     item.classList.remove('active');
//   }
// });
// }



// variable value
//  function variablevalue(){
//   var dropdown=1;
//  }

// lokesh code


// Add an event listener to the dropdown
// dropdown.addEventListener("click", function() {
//     // If the dropdown is open, store its state in local storage
//     if (dropdown.size == 1) {
//         localStorage.setItem("dropdownWasOpen", "true");
//     } else {
//         localStorage.removeItem("dropdownWasOpen");
//     }
// });

// usertable/clienttable destroy

const myLink = document.getElementById("myLink");
const myButton = document.getElementById("myButton");

myLink.addEventListener("click", function (event) {
  event.preventDefault(); // prevent default behavior of following the link
  myButton.dataset.href = myLink.href; // set the href value as data-href attribute
});

myButton.addEventListener('click', function (event) {
  event.preventDefault(); // prevent default behavior of submitting the form
  const href = myButton.dataset.href;
  if (href) {
    window.location.href = href; // navigate to the URL stored in data-href
  }
});

