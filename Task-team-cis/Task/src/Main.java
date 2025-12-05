void main() {
    FrozenTunnel tunnel = new FrozenTunnel();
    String test1 = "I___I_I";
    System.out.println("Example 1 Input: " + test1);
    System.out.println("Melted: " + tunnel.countMeltedIce(test1)); // Output should be 2

    System.out.println("-----------------");

    // Example 2
    String test2 = "I__I__I";
    System.out.println("Example 2 Input: " + test2);
    System.out.println("Melted: " + tunnel.countMeltedIce(test2)); // Output should be 0

}