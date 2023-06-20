let button_to_add_patch = document.querySelector(".button_to_add_patch");

let alert_block = document.querySelector(".alert_block");

let modal = document.querySelector(".modal");
let modal_path_to_func_input = document.querySelector(".path_to_func");
let modal_executable_module_name_input = document.querySelector(
  ".executable_module_name"
);
let modal_line_where_func_executed_input = document.querySelector(
  ".line_where_func_executed_input"
);
let modal_decorator_inner_func_input = document.querySelector(
  ".decorator_inner_func_input"
);
let modal_is_method_input_checkbox = document.querySelector(
  ".is_method_input_checkbox"
);

let modal_close_button = document.querySelector(".close_modal_button");
let modal_approve_button = document.querySelector(".approve_modal_button");

let table_body = document.querySelector(".patchers_table_body");

// START on click section
function on_click_to_delete_func_patch(func_patcher_pk, t_row) {
  fetch("/func_patcher_api/func_patcher_detail/", {
    method: "DELETE",
    body: JSON.stringify({ func_patcher_pk: func_patcher_pk }),
    headers: { "Content-Type": "application/json" },
  }).then((response) => {
    if (response.ok) {
      delete_row_from_table(t_row);
    }
  });
}

function on_click_to_change_active_state(func_patcher_pk, tr_el) {
  fetch("/func_patcher_api/func_patcher_detail/", {
    method: "PUT",
    body: JSON.stringify({ func_patcher_pk: func_patcher_pk }),
    headers: { "Content-Type": "application/json" },
  })
    .then((response) => {
      if (response.ok) {
        change_is_active_state_to_opposite(tr_el);
      }
      return Promise.reject(response);
    })
    .catch((response) => {
      if (response.status == 400) {
        response.json().then((invalid_response) => {
          create_and_add_alert_block(invalid_response["exception"]);
        });
      }
    });
}
// END on click section

const zip = (...arr) => {
  const zipped = [];
  arr.forEach((element, ind) => {
    element.forEach((el, index) => {
      if (!zipped[index]) {
        zipped[index] = [];
      }
      if (!zipped[index][ind]) {
        zipped[index][ind] = [];
      }
      zipped[index][ind] = el || "";
    });
  });
  return zipped;
};

function create_and_add_alert_block(alert_message) {
  let new_alert = document.createElement("div");
  new_alert.innerHTML = `
                <div class="alert alert-danger" role="alert">
                ${alert_message} 
                <button type="button" class="btn-close" data-bs-dismiss="alert" aria-label="Close"></button>
                </div>
                `;
  alert_block.append(new_alert);
}

function change_is_active_state_to_opposite(tr_el) {
  let opposite_value = (+!Boolean(Number(tr_el.innerText))).toString();
  tr_el.innerText = opposite_value;
  tr_el.classList.toggle("active_true");
  tr_el.classList.toggle("active_false");
}

function delete_row_from_table(row) {
  row.remove();
}

function set_on_click_to_trow_buttons() {
  let buttons_to_change_is_active_state = document.querySelectorAll(
    ".button_to_change_is_active_state"
  );
  let buttons_to_delete_patcher = document.querySelectorAll(
    ".button_to_delete_patcher"
  );
  let is_active_trs = document.querySelectorAll(
    ".patcher_data_is_active_field"
  );
  let t_rows = document.querySelectorAll(".patcher_data");
  for (let [
    t_row,
    button_to_change_is_active_state,
    button_to_delete_patcher,
    is_active_tr,
  ] of zip(
    t_rows,
    buttons_to_change_is_active_state,
    buttons_to_delete_patcher,
    is_active_trs
  )) {
    button_to_change_is_active_state.addEventListener("click", () => {
      on_click_to_change_active_state(t_row.id, is_active_tr);
    });
    button_to_delete_patcher.addEventListener("click", () =>
      on_click_to_delete_func_patch(t_row.id, t_row)
    );
  }
}

function clear_modal_inputs() {
  modal_path_to_func_input.value = "";
  modal_executable_module_name_input.value = "";
  modal_line_where_func_executed_input.value = "";
  modal_decorator_inner_func_input.value = "";
  modal_is_method_input_checkbox.checked = false;
}

function create_row_with_patch_data(
  path_to_func,
  executable_module_name,
  line_number_where_func_executed,
  decorator_inner_func,
  is_method,
  new_patch_pk
) {
  let t_row = document.createElement("tr");
  t_row.id = new_patch_pk;
  t_row.classList.add("patcher_data");
  t_row.innerHTML = `
    <td class="patcher_data_is_active_field active_true">1</td>
    <td>${path_to_func}</td>
    <td>${executable_module_name}</td>
    <td>${line_number_where_func_executed}</td>
    <td>${is_method ? 1 : 0}</td>
    <td>
        <pre>${decorator_inner_func}</pre>
    </td>
    <td>
        <button type="button" class="btn btn-primary button_to_change_is_active_state">
            change status
        </button>
    </td>
    <td>
        <button type="button" class="btn btn-danger button_to_delete_patcher">
            delete
        </button>
    </td>`;

  table_body.appendChild(t_row);

  let buttons_to_delete_patcher = document.querySelectorAll(
    ".button_to_delete_patcher"
  );
  let new_button_to_delete_patcher =
    buttons_to_delete_patcher[buttons_to_delete_patcher.length - 1];
  new_button_to_delete_patcher.addEventListener("click", () => {
    on_click_to_delete_func_patch(t_row.id, t_row);
  });

  let is_active_trs = document.querySelectorAll(
    ".patcher_data_is_active_field"
  );
  let last_is_active_tr = is_active_trs[is_active_trs.length - 1];
  let buttons_to_change_is_active_state = document.querySelectorAll(
    ".button_to_change_is_active_state"
  );
  let new_button_to_change_active_state =
    buttons_to_change_is_active_state[
      buttons_to_change_is_active_state.length - 1
    ];
  new_button_to_change_active_state.addEventListener("click", () => {
    on_click_to_change_active_state(t_row.id, last_is_active_tr);
  });
}

modal_close_button.addEventListener("click", () => {
  clear_modal_inputs();
});

modal_approve_button.addEventListener("click", () => {
  fetch("/func_patcher_api/func_patcher_detail/", {
    method: "POST",
    body: JSON.stringify({
      path_to_func: modal_path_to_func_input.value,
      executable_module_name: modal_executable_module_name_input.value,
      line_number_where_func_executed:
        modal_line_where_func_executed_input.value,
      decorator_inner_func: modal_decorator_inner_func_input.value,
      is_method: modal_is_method_input_checkbox.checked,
    }),
    headers: { "Content-Type": "application/json" },
  })
    .then((response) => {
      if (response.ok) {
        return response.json();
      }
      return Promise.reject(response);
    })
    .then((response) => {
      create_row_with_patch_data(
        modal_path_to_func_input.value,
        modal_executable_module_name_input.value,
        modal_line_where_func_executed_input.value,
        modal_decorator_inner_func_input.value,
        modal_is_method_input_checkbox.checked,
        response["created_patch_data_pk"]
      );
      clear_modal_inputs();
    })
    .catch((response) => {
      if (response.status == 400) {
        response.json().then((invalid_response) => {
          create_and_add_alert_block(invalid_response["exception"]);
        });
      }
    });
});

set_on_click_to_trow_buttons();
