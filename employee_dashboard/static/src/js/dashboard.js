/**@odoo-module **/
import { registry } from "@web/core/registry";
import { Component } from  "@odoo/owl";
import { useService } from "@web/core/utils/hooks";
import { user } from "@web/core/user";
import { renderToFragment } from "@web/core/utils/render";

const actionRegistry = registry.category("actions");
//console.log(user.hasGroup('hr.group_hr_manager'))
class EmployeeDashboard extends Component {
    setup() {
         super.setup()
         this.orm = useService('orm')
         this._fetch_data()
         this.action = useService("action")
         this.orm = useService("orm")
   }
  async _fetch_data(){
        this.user = await user.hasGroup('hr.group_hr_manager')
        console.log(this)
        if(this.user){
            this.checking = 'abcd'
//            var laptop = 'a'
//            const infoContent = renderToFragment(
//                "employee_dashboard.EmployeeDashboard",
//                {
//                    infoKey: laptop,
//                }
//            );
        }
        var employee = await this.orm.searchRead("hr.employee", [['user_id', '=', user.userId]], [])
        var child_ids = []
        var parent_id = []
        if(employee[0].child_ids) {
            for (let i=0; i < employee.length; i++){
                child_ids.push(employee[i].child_ids)
                parent_id.push(employee[i].parent_id)
            }
        }
        var child_array = child_ids[0];
        var parent_array = parent_id[0];
        if (parent_array){
            document.getElementById('parent_org').append(parent_array[1]);
            document.getElementById('sub_head').innerHTML +=(`<li class="o_org_chart_entry o_org_chart_entry_sub o_treeEntry d-flex position-relative py-2 overflow-visible">` + employee[0].display_name + `</li>`);
        }else{
            document.getElementById('sub_head').append(employee[0].display_name);
        }
        for (let i=0; i < child_array.length; i++){
            var child_data = await this.orm.searchRead("hr.employee", [["id", "=", child_array[i]]], [])
            document.getElementById('chart_list').innerHTML +=(`<li class="o_org_chart_entry o_org_chart_entry_sub o_treeEntry d-flex position-relative py-2 overflow-visible">` + child_data[0].display_name + `</li>`);
        }
        this.orm.call("hr.employee", "get_tiles_data", [], {}).then(function(result){
           document.getElementById('attendance').append(result.total_attendance);
           document.getElementById('leaves').append(result.total_leave);
           document.getElementById('project').append(result.total_project);
           document.getElementById('information').innerHTML +=(result.employee_info.name + `<br><div style=font-size:15px;>` + employee[0].job_id[1] + `</div>`);
           document.getElementById('information_data').append('Experience: ' + result.employee_info.experience + ' years');
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
   employeeTileClick(){
        this.action.doAction({
            type: 'ir.actions.act_window',
            res_model: 'hr.employee',
            views: [[false, 'kanban']],
            target: 'current',
       })
//        document.getElementById('personal_info_tile').style.display = 'none'
//        document.getElementById('org_chart').style.display = 'none'
//        document.getElementById('attendance_tile').style.display = 'none'
//        document.getElementById('leave_tile').style.display = 'none'
//        document.getElementById('project_tile').style.display = 'none'
   }
   orgChartClick(){
        this.action.doAction({
                type: 'ir.actions.act_window',
                res_model: 'hr.employee',
                views: [[false, 'hierarchy']],
                target: 'current',
        })
   }
}
EmployeeDashboard.template = "employee_dashboard.EmployeeDashboard";
actionRegistry.add("employee_dashboard_tag", EmployeeDashboard);
