import java.sql.ResultSet;
import java.util.ArrayList;
import java.util.regex.Matcher;
import java.util.regex.Pattern;


public class introduction_operator {
	public static void main(String[] args){
		place_spider spider = new place_spider();
		String s = "select * from place";
		String url = "";
		ArrayList<String> errorIntrodution_ID = new ArrayList<String>();
		try{
			ResultSet rs = spider.statement.executeQuery(s);
			while(rs.next()){
				String id = rs.getString("ID");
				String intro = rs.getString("introduction");
				String regexp1 ="<a href=\".*?\" class=\"show-full\">展开</a>";
				Pattern p1 = Pattern.compile(regexp1);
				Matcher m1 = p1.matcher(intro);
				if(m1.find()){
					errorIntrodution_ID.add(id);
				}
			}
		}catch(Exception e){
			e.printStackTrace();
		}
		for(String id : errorIntrodution_ID){
			s="delete from place where ID ="+id;
			try{
				spider.statement.executeUpdate(s);
			}catch(Exception e){
				e.printStackTrace();
			}
			url = "http://trip.douban.com/place/"+id+"/";
			spider.getInfo(url);
		}
	}
}
