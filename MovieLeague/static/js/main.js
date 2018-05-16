function addinputFields(users, movies){
    var TopDiv = document.createElement('div');
    TopDiv.className = "fields";
    TopDiv.id = "equalqwidthfields_"+count;
    var InnerDiv = document.createElement('div');
    InnerDiv.className = "eight wide field";
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
    InnerDiv_m.className = "seven wide field";
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

    var removeDiv = document.createElement('div');
    removeDiv.className = "one wide field";
    /*var removeButton = document.createElement('button');
    removeButton.className = "ui icon button";
    removeButton.id = "remove_".concat(count);
    removeButton.onclick = function() {alert('hi')}*/
    var removeIcon = document.createElement('i');
    removeIcon.className = "big minus square outline icon";
    removeIcon.onclick = function() {
        var elem = TopDiv.id;
        $('#'+elem).remove();
    };
    //removeButton.appendChild(removeIcon);
    //removeDiv.appendChild(removeButton);
    removeDiv.appendChild(removeIcon)


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

    TopDiv.appendChild(removeDiv);

    count++;
    formgroup.appendChild(TopDiv);

    $(function() {
        $('.ui.dropdown')
            .dropdown();
    });
}

/*
	A simple, lightweight jQuery plugin for creating sortable tables.
	https://github.com/kylefox/jquery-tablesort
	Version 0.0.11
*/

(function($) {
	$.tablesort = function ($table, settings) {
		var self = this;
		this.$table = $table;
		this.$thead = this.$table.find('thead');
		this.settings = $.extend({}, $.tablesort.defaults, settings);
		this.$sortCells = this.$thead.length > 0 ? this.$thead.find('th:not(.no-sort)') : this.$table.find('th:not(.no-sort)');
		this.$sortCells.on('click.tablesort', function() {
			self.sort($(this));
		});
		this.index = null;
		this.$th = null;
		this.direction = null;
	};

	$.tablesort.prototype = {

		sort: function(th, direction) {
			var start = new Date(),
				self = this,
				table = this.$table,
				rowsContainer = table.find('tbody').length > 0 ? table.find('tbody') : table,
				rows = rowsContainer.find('tr').has('td, th'),
				cells = rows.find(':nth-child(' + (th.index() + 1) + ')').filter('td, th'),
				sortBy = th.data().sortBy,
				sortedMap = [];

			var unsortedValues = cells.map(function(idx, cell) {
				if (sortBy)
					return (typeof sortBy === 'function') ? sortBy($(th), $(cell), self) : sortBy;
				return ($(this).data().sortValue != null ? $(this).data().sortValue : $(this).text());
			});
			if (unsortedValues.length === 0) return;

			//click on a different column
			if (this.index !== th.index()) {
				this.direction = 'asc';
				this.index = th.index();
			}
			else if (direction !== 'asc' && direction !== 'desc')
				this.direction = this.direction === 'asc' ? 'desc' : 'asc';
			else
				this.direction = direction;

			direction = this.direction == 'asc' ? 1 : -1;

			self.$table.trigger('tablesort:start', [self]);
			self.log("Sorting by " + this.index + ' ' + this.direction);

			// Try to force a browser redraw
			self.$table.css("display");
			// Run sorting asynchronously on a timeout to force browser redraw after
			// `tablesort:start` callback. Also avoids locking up the browser too much.
			setTimeout(function() {
				self.$sortCells.removeClass(self.settings.asc + ' ' + self.settings.desc);
				for (var i = 0, length = unsortedValues.length; i < length; i++)
				{
					sortedMap.push({
						index: i,
						cell: cells[i],
						row: rows[i],
						value: unsortedValues[i]
					});
				}

				sortedMap.sort(function(a, b) {
					return self.settings.compare(a.value, b.value) * direction;
				});

				$.each(sortedMap, function(i, entry) {
					rowsContainer.append(entry.row);
				});

				th.addClass(self.settings[self.direction]);

				self.log('Sort finished in ' + ((new Date()).getTime() - start.getTime()) + 'ms');
				self.$table.trigger('tablesort:complete', [self]);
				//Try to force a browser redraw
				self.$table.css("display");
			}, unsortedValues.length > 2000 ? 200 : 10);
		},

		log: function(msg) {
			if(($.tablesort.DEBUG || this.settings.debug) && console && console.log) {
				console.log('[tablesort] ' + msg);
			}
		},

		destroy: function() {
			this.$sortCells.off('click.tablesort');
			this.$table.data('tablesort', null);
			return null;
		}

	};

	$.tablesort.DEBUG = false;

	$.tablesort.defaults = {
		debug: $.tablesort.DEBUG,
		asc: 'sorted ascending',
		desc: 'sorted descending',
		compare: function(a, b) {
			if (a > b) {
				return 1;
			} else if (a < b) {
				return -1;
			} else {
				return 0;
			}
		}
	};

	$.fn.tablesort = function(settings) {
		var table, sortable, previous;
		return this.each(function() {
			table = $(this);
			previous = table.data('tablesort');
			if(previous) {
				previous.destroy();
			}
			table.data('tablesort', new $.tablesort(table, settings));
		});
	};

})(window.Zepto || window.jQuery);

