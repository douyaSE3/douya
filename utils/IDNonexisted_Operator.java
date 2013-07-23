import java.sql.ResultSet;
import java.util.ArrayList;
import java.util.regex.Matcher;
import java.util.regex.Pattern;


public class IDNonexisted_Operator {
	public static void main(String[] args){
		place_spider spider = new place_spider();
		String s = "select * from place";
		String url = "";
		ArrayList<String> existed_ID = new ArrayList<String>();
		try{
			ResultSet rs = spider.statement.executeQuery(s);
			while(rs.next()){
				String id = rs.getString("ID");
				existed_ID.add(id);
			}
		}catch(Exception e){
			e.printStackTrace();
		}
		for(int i=1000000;i<1005553;i++){
			String id=""+i;
			if(!existed_ID.contains(id)){
				url = "http://trip.douban.com/place/"+id+"/";
				spider.getInfo(url);
			}
		}
	}
}
