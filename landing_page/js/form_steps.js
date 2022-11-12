// the form
var registration_form = document.querySelector('.js-registration-form');
// the steps bar
var steps_container = document.querySelector('.steps-container');

// get all the steps from the stepbar as an array to check in which step we are
var steps_array = [...steps_container.querySelectorAll('.step')];

// this function will remove .active class from all the steps
function clear_active_buttons(steps) {
    steps.forEach(step => {
      if( step.classList.contains('active') ) {
        step.classList.remove('active');
      }
    });
  }

function addActive(step) {
    steps_array.forEach(stepsTab => {
  });
} 

// remove .completed class from all the steps --we need this when the form return to the first step--
function remove_all_steps() {
    for( var i = 0; i < steps_array.length; i++ ) {
        steps_array[i].classList.remove('completed');
    }
}

// find the active tab and add a class in each previus step
function add_class_to_completed_steps(current_tab) {
  
    //   the index of the step who is clicked
    var tabs_index = steps_array.indexOf(current_tab);
    
    // add .completed to all previous steps     
    for( var i = 0; i < steps_array.indexOf(current_tab); i++ ) {
    steps_array[i].classList.add('completed');
    }
    
    // remove .completed from all the next steps and the current step     
    for( var j = tabs_index; j < steps_array.length; j++ ) {
    if( steps_array[j].classList.contains('completed') ) {
        steps_array[j].classList.remove('completed');
    }
    }
}


if ( !(registration_form === 0) & !(steps_container === 0)) {
    // check in which step is the form
    var form_step = registration_form.getAttribute('data-step');

    // get the same step from the stepbar
    var active_step = steps_container.querySelector("[data-step='" + form_step + "']");

    // if the form is above the first step change active and complete class
    var current_step = steps_array.indexOf(active_step);
    if( current_step > 0 ) {

        // add .active to current step and remove it from the non active
        add_class_to_completed_steps(active_step);
        addActive(active_step);
    }

    steps_array.forEach(step => {
        if( !( steps_array.indexOf(step) === current_step )) {
          step.classList.remove('active');
        }
        else {step.classList.add('active');}
    });
} 
