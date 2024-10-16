/**@odoo-module **/
import { registry } from "@web/core/registry";
import { useState, Component, onWillStart } from  "@odoo/owl";
import { useService } from "@web/core/utils/hooks";
import { user } from "@web/core/user";
import { renderToFragment } from "@web/core/utils/render";

const actionRegistry = registry.category("actions");
class EmployeeDashboard extends Component {
    setup() {
         super.setup()
         this.orm = useService('orm')
         this.action = useService("action")
         this.orm = useService("orm")
         this.state = useState({
            value: "",
            user_name: "",
            user_val: "",
            user_job: "",
            emp_value: "",
        })
         onWillStart(async () => {
            this.isEmployeeManager = await user.hasGroup("base.group_system");
         });
         this._fetch_data()
    }
    async _fetch_data(){
        this.state.value = await this.orm.searchRead("hr.employee", [], [])
        var obj = await this.state.value
        var user_data = []
        var child_list = []
        for (let i=0; i < obj.length; i++){
            if (obj[i].user_id[0] == user.userId){
                user_data.push(obj[i])
                child_list.push(obj[i].child_ids)
            }
        }
        this.state.user_val = user_data[0]
        this.state.user_name = user_data[0].display_name
        this.state.user_job = user_data[0].job_id[1]
        var child_array = child_list[0]
        for (let i=0; i < child_array.length; i++){
            var child_data = await this.orm.searchRead("hr.employee", [["id", "=", child_array[i]]], [])
            document.getElementById('chart_list').innerHTML +=(`<li class="o_org_chart_entry o_org_chart_entry_sub o_treeEntry d-flex position-relative py-2 overflow-visible">` + child_data[0].display_name + `</li>`);
        }
        this.orm.call("hr.employee", "get_tiles_data", [], {}).then(function(result){
        document.getElementById('experience').append('Experience: ' + result.employee_info.experience + ' years');
        document.getElementById('attendance').append(result.total_attendance);
        document.getElementById('leaves').append(result.total_leave);
        document.getElementById('project').append(result.total_project);
        });
   };
   attendanceTileClick(){
        this.action.doAction({
                type: 'ir.actions.act_window',
                res_model: 'hr.attendance',
                domain: [["employee_id.user_id", "=", user.userId]],
                views: [[false, 'list'], [false, 'form']],
                target: 'current',
            })
   }
   leaveTileClick(){
        this.action.doAction({
                type: 'ir.actions.act_window',
                res_model: 'hr.leave',
                domain: [["employee_id.user_id", "=", user.userId]],
                views: [[false, 'list'], [false, 'form']],
                target: 'current',
            })
   }
   projectTileClick(){
        this.action.doAction({
                type: 'ir.actions.act_window',
                res_model: 'project.project',
                domain: [["user_id", "=", user.userId]],
                views: [[false, 'list'], [false, 'form']],
                target: 'current',
            })
   }
   personalInfoTileClick(){
        var action_employee = this.action
        this.orm.call("hr.employee", "get_tiles_data", [], {}).then(function(result){
            var eid = result.employee_info['id']
            action_employee.doAction({
                type: 'ir.actions.act_window',
                res_model: 'hr.employee',
                res_id: eid,
                views: [[false, "form"]],
                target: 'current',
            })
        })
   }
   orgChartClick(){
        this.action.doAction({
                type: 'ir.actions.act_window',
                res_model: 'hr.employee',
                views: [[false, 'hierarchy']],
                target: 'current',
        })
   }
   async empClick(e){
        var target = e.target
        document.getElementById('experience').style.display= "none";
//        document.getElementById("dashboard").style.display = "none";
        console.log(e)
        var emp_id = target.children[0].innerText;
        this.state.emp_value = await this.orm.searchRead("hr.employee", [["id", "=", emp_id]], [])
        this.state.user_name = this.state.emp_value[0].display_name
        this.state.user_job = this.state.emp_value[0].job_id[1]
        console.log(this.state.emp_value,'//val')
   }
}
EmployeeDashboard.template = "employee_dashboard.EmployeeDashboard";
actionRegistry.add("employee_dashboard_tag", EmployeeDashboard);
