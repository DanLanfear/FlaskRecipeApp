$(function() {
    $("div[data-toggle=fieldset]").each(function() {
        var $this = $(this);
            
            //Add new entry
        $this.find("button[data-toggle=fieldset-add-row]").click(function() {
            var target = $($(this).data("target"))
            console.log(target);
            var oldrow = target.find("div[data-toggle=fieldset-entry]:last");
            var row = oldrow.clone(true, true);
            console.log(row.find(":input")[0]);
            var elem_id = row.find(":input")[0].id;
            var elem_num = parseInt(elem_id.replace(/.*-(\d{1,4})-.*/m, '$1')) + 1;
            row.attr('data-id', elem_num);
            row.find(":input").each(function() {
                console.log(this);
                var id = $(this).attr('id').replace('-' + (elem_num - 1) + '-', '-' + (elem_num) + '-');
                $(this).attr('name', id).attr('id', id).val('').removeAttr("checked");
            });
            oldrow.after(row);
        }); //End add new entry

                //Remove row
        $this.find("button[data-toggle=fieldset-remove-row]").click(function() {
            if($this.find("div[data-toggle=fieldset-entry]").length > 1) {
                var thisRow = $(this).closest("div[data-toggle=fieldset-entry]");
                thisRow.remove();
            }
        }); //End remove row
    });
});



$(function() {
    $("div[data-toggle=fieldset]").each(function() {
        var $this = $(this);
            
            //Add new entry
        $this.find("button[data-toggle=tag-add]").click(function() {
            var target = $($(this).data("target"))
            console.log(target);
            var oldentry = target.find("ul[data-toggle=tag]:last");
            var entry = oldentry.clone(true, true);
            console.log(entry.find(":input")[0]);
            var elem_id = entry.find(":input")[0].id;
            var elem_num = parseInt(elem_id.replace(/.*-(\d{1,4})-.*/m, '$1')) + 1;
            entry.attr('data-id', elem_num);
            entry.find(":input").each(function() {
                console.log(this);
                var id = $(this).attr('id').replace('-' + (elem_num - 1) + '-', '-' + (elem_num) + '-');
                $(this).attr('name', id).attr('id', id).val('').removeAttr("checked");
            });
            oldentry.after(entry);
        }); //End add new entry

        //Remove row
        $this.find("li[data-toggle=tag-remove]").click(function() {
            // target_remove = $this.find("li[data-toggle=tag-remove]");
            // target_remove.remove();
            $(this).remove();
        }); //End remove row
    });
});