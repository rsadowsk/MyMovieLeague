function addinputFields(users, movies){
    var TopDiv = document.createElement('div');
    TopDiv.className = "equal width fields";
    TopDiv.id = "equalqwidthfields";
    var InnerDiv = document.createElement('div');
    InnerDiv.className = "field";
    var secondInnerDiv = document.createElement('div');
    secondInnerDiv.className = "ui search selection dropdown";
    var firstInput = document.createElement('input');
    firstInput.id = "UsersDefaultNameInput".concat(count);
    firstInput.name = "name";
    firstInput.type = "name";
    var secondInput = document.createElement('input');
    secondInput.className = 'search';
    secondInput.setAttribute("autocomplete", "off");
    secondInput.setAttribute("tabindex", "0");
    var icon = document.createElement('i');
    icon.className = "dropdown icon";
    var thirdInnerDiv = document.createElement('div');
    thirdInnerDiv.className = "default text";
    thirdInnerDiv.id = "UsersDefaultNameDiv".concat(count);
    var fourthInnerDiv = document.createElement('div');
    fourthInnerDiv.className = "menu";
    fourthInnerDiv.setAttribute("tabindex", "-1");
    console.log(users.replace(/&#34;/g,'"'));
    JSON.parse(users.replace(/&#34;/g,'"'), function(key, value) {
        if (key.length > 0) {
            var forDiv = document.createElement('div');
            forDiv.className = 'item';
            forDiv.setAttribute("data-value", key);
            forDiv.innerHTML = value;
            fourthInnerDiv.appendChild(forDiv);
            }
        }
    );
    var InnerDiv_m = document.createElement('div');
    InnerDiv_m.className = "field";
    var secondInnerDiv_m = document.createElement('div');
    secondInnerDiv_m.className = "ui search selection dropdown";
    var firstInput_m = document.createElement('input');
    firstInput_m.id = "UsersDefaultMovieInput".concat(count);
    firstInput_m.name = "name";
    firstInput_m.type = "name";
    var secondInput_m = document.createElement('input');
    secondInput_m.className = 'search';
    secondInput_m.setAttribute("autocomplete", "off");
    secondInput_m.setAttribute("tabindex", "0");
    var icon_m = document.createElement('i');
    icon_m.className = "dropdown icon";
    var thirdInnerDiv_m = document.createElement('div');
    thirdInnerDiv_m.className = "default text";
    thirdInnerDiv_m.id = "UsersDefaultMovieDiv".concat(count);
    var fourthInnerDiv_m = document.createElement('div');
    fourthInnerDiv_m.className = "menu";
    fourthInnerDiv_m.setAttribute("tabindex", "-1");
    console.log(movies.replace(/&#34;/g,'"'));
    JSON.parse(movies.replace(/&#34;/g,'"'), function(key, value) {
        if (key.length > 0) {
            var forDiv = document.createElement('div');
            forDiv.className = 'item';
            forDiv.setAttribute("data-value", key);
            forDiv.innerHTML = value;
            fourthInnerDiv_m.appendChild(forDiv);
            }
        }
    );
    secondInnerDiv.appendChild(firstInput);
    secondInnerDiv.appendChild(icon);
    secondInnerDiv.appendChild(secondInput);
    secondInnerDiv.appendChild(thirdInnerDiv);
    secondInnerDiv.appendChild(fourthInnerDiv);
    InnerDiv.appendChild(secondInnerDiv);
    TopDiv.appendChild(InnerDiv);

    secondInnerDiv_m.appendChild(firstInput_m);
    secondInnerDiv_m.appendChild(icon_m);
    secondInnerDiv_m.appendChild(secondInput_m);
    secondInnerDiv_m.appendChild(thirdInnerDiv_m);
    secondInnerDiv_m.appendChild(fourthInnerDiv_m);
    InnerDiv_m.appendChild(secondInnerDiv_m);
    TopDiv.appendChild(InnerDiv_m);
    count++;
    formgroup.appendChild(TopDiv);
    $(function() {
    $('.ui.dropdown')
        .dropdown();
});
}

