frappe.ui.form.on('Work Order', {
    setup: function(frm) {
        // Completely overwrite the standard ERPNext handler to avoid duplicates or DOM fighting
        frappe.ui.form.handlers["Work Order"]["show_progress_for_operations"] = [function(frm) {
            if (frm.doc.operations && frm.doc.operations.length) {
                let progress_class = {
                    "Work in Progress": "progress-bar-warning",
                    Completed: "progress-bar-success",
                };

                let bars = [];
                let message = "";
                let title = "";
                let status_wise_oprtation_data = {};
                let total_completed_qty = frm.doc.qty * frm.doc.operations.length;

                frm.doc.operations.forEach((d) => {
                    // FIX: Treat 'Completed' operations as having fulfilled the total qty
                    let qty = d.status === "Completed" ? frm.doc.qty : flt(d.completed_qty);

                    if (!status_wise_oprtation_data[d.status]) {
                        status_wise_oprtation_data[d.status] = [qty, d.operation];
                    } else {
                        status_wise_oprtation_data[d.status][0] += qty;
                        status_wise_oprtation_data[d.status][1] += ", " + d.operation;
                    }
                });

                for (let key in status_wise_oprtation_data) {
                    title = __("{0} Operations: {1}", [key, status_wise_oprtation_data[key][1].bold()]);
                    bars.push({
                        title: title,
                        width: (status_wise_oprtation_data[key][0] / total_completed_qty) * 100 + "%",
                        progress_class: progress_class[key],
                    });

                    message += title + ". ";
                }

                // Add progress chart with distinct title so it replaces cleanly
                frm.dashboard.add_progress(__("Status"), bars, message);
            }
        }];
    }
});
