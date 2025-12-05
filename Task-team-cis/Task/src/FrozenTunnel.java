public class FrozenTunnel {

    public static int countMeltedIce(String tunnel) {
        int meltedCount = 0;
        int airStreak = 0;


        for (char cell : tunnel.toCharArray()) {
            if (cell == '_') {

                airStreak++;
            } else if (cell == 'I') {

                if (airStreak >= 3) {
                    meltedCount++;

                    airStreak++;
                } else {

                    airStreak = 0;
                }
            }
        }

        return meltedCount;
    }
}